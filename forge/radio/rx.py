#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import signal
from pathlib import Path
from argparse import ArgumentParser

from gnuradio import gr, blocks, uhd

from utils.logger import setup_logger
from utils.sigmf_writer import write_sigmf


class rx_record(gr.top_block):
    def __init__(self, usrp_args, freq, rate, gain, out_path, antenna="RX2"):
        super().__init__("RX record")

        self.src = uhd.usrp_source(
            usrp_args,
            uhd.stream_args(cpu_format="fc32", channels=[0]),
        )
        self.src.set_clock_source("internal", 0)
        self.src.set_samp_rate(rate)
        self.src.set_center_freq(freq, 0)
        self.src.set_gain(gain, 0)
        self.src.set_antenna(antenna, 0)

        self.sink = blocks.file_sink(gr.sizeof_gr_complex, out_path, False)
        self.sink.set_unbuffered(False)

        self.connect(self.src, self.sink)


def parse_args():
    p = ArgumentParser()
    p.add_argument("--serial", type=str, default=os.environ.get("USRP_SERIAL", ""))
    p.add_argument("--addr", type=str, default="")
    p.add_argument("--freq", type=float, default=float(os.environ.get("RX_FREQ", "2.45e9")))
    p.add_argument("--rate", type=float, default=float(os.environ.get("RX_RATE", "2.5e5")))
    p.add_argument("--gain", type=float, default=float(os.environ.get("RX_GAIN", "15")))
    p.add_argument("--secs", type=float, default=float(os.environ.get("RX_SECS", "5")))
    p.add_argument("--antenna", type=str, default=os.environ.get("RX_ANT", "RX2"))

    p.add_argument("--base", type=str, default=os.environ.get(
        "SIGMF_BASE",
        "/cortexlab/homes/andrea_joly/CorteXForge/out/test"
    ))
    return p.parse_args()


def main():
    logger = setup_logger()
    args = parse_args()

    base = Path(args.base)
    base.parent.mkdir(parents=True, exist_ok=True)

    # temp raw file (will be renamed to .sigmf-data)
    raw_path = base.with_suffix(".cf32")

    # UHD args: SERIAL first (important on cortexlab)
    if args.serial:
        usrp_args = f"serial={args.serial}"
    elif args.addr:
        usrp_args = args.addr
    else:
        usrp_args = ""

    logger.info(f"usrp_args={usrp_args!r} freq={args.freq} rate={args.rate} gain={args.gain} secs={args.secs} ant={args.antenna}")
    logger.info(f"base={base}")

    tb = rx_record(
        usrp_args=usrp_args,
        freq=args.freq,
        rate=args.rate,
        gain=args.gain,
        out_path=str(raw_path),
        antenna=args.antenna,
    )

    stop_flag = {"stop": False}
    def handler(sig, frame): stop_flag["stop"] = True
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    tb.start()
    t0 = time.time()
    while not stop_flag["stop"] and (time.time() - t0) < args.secs:
        time.sleep(0.05)
    tb.stop()
    tb.wait()

    # Sanity size check (cf32 => 8 bytes per sample)
    nsamps = int(args.rate * args.secs)
    expected = nsamps * 8
    size = raw_path.stat().st_size if raw_path.exists() else 0
    logger.info(f"Raw wrote: {raw_path} size={size} expected≈{expected}")

    # Write SigMF (renames raw to .sigmf-data + writes .sigmf-meta)
    data_path, meta_path = write_sigmf(
        base_path=str(base),
        data_file=str(raw_path),
        sample_rate=args.rate,
        center_freq=args.freq,
        datatype="cf32_le",
        description="Noise capture",
        hardware="USRP (Cortexlab)",
        usrp_serial=args.serial or None,
        antenna=args.antenna,
        gain=args.gain,
    )
    logger.info(f"SigMF files written: {data_path} and {meta_path}")


if __name__ == "__main__":
    main()
