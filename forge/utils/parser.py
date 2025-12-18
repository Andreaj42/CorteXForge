import os
import argparse

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="CorteXForge",
        description="CorteXlab Dataset Generator"
    )

    parser.add_argument(
        "--role",
        default=os.environ.get("CORTEXFORGE_ROLE", "rx"),
        choices=["rx", "tx"],
        help="Radio role for this node (rx=receiver, tx=transmitter)"
    )

    return parser


def parse_args():
    parser = build_parser()
    return parser.parse_known_args()
