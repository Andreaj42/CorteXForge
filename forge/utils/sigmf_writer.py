import json
from datetime import datetime, timezone
from pathlib import Path


def write_sigmf(
    base_path: str,
    data_file: str,
    sample_rate: float,
    center_freq: float,
    datatype: str = "cf32_le",
    description: str = "CorteXForge capture",
    author: str = "CorteXForge",
    hardware: str | None = None,
    usrp_serial: str | None = None,
    antenna: str | None = None,
    gain: float | None = None,
):
    """
    base_path: path without extension, e.g. /.../out/noise_node6
    data_file: existing IQ file path (fc32 raw)
    Creates:
      - base_path.sigmf-data  (binary copy or rename)
      - base_path.sigmf-meta  (json)
    """
    base = Path(base_path)
    data_src = Path(data_file)

    meta_path = base.with_suffix(".sigmf-meta")
    data_path = base.with_suffix(".sigmf-data")

    # Move (rename) the data to .sigmf-data if needed
    if data_src.resolve() != data_path.resolve():
        data_path.parent.mkdir(parents=True, exist_ok=True)
        data_src.replace(data_path)

    meta = {
        "global": {
            "core:datatype": datatype,
            "core:sample_rate": float(sample_rate),
            "core:description": description,
            "core:author": author,
            "core:recorder": "CorteXForge",
            "core:version": "1.0.0",
        },
        "captures": [
            {
                "core:sample_start": 0,
                "core:frequency": float(center_freq),
                "core:datetime": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            }
        ],
        "annotations": []
    }

    # Useful optional fields (non-core, still fine)
    extras = {}
    if hardware: extras["cortexforge:hardware"] = hardware
    if usrp_serial: extras["cortexforge:usrp_serial"] = usrp_serial
    if antenna: extras["cortexforge:antenna"] = antenna
    if gain is not None: extras["cortexforge:gain_db"] = float(gain)
    if extras:
        meta["global"].update(extras)

    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True))
    return str(data_path), str(meta_path)
