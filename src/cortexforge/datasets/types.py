from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class SplitManifest:
    recordings: list[str]


@dataclass(slots=True)
class GeneratorManifest:
    name: str
    version: str


@dataclass(slots=True)
class DatasetManifest:
    name: str
    version: str
    description: str
    format: str
    generator: GeneratorManifest
    splits: dict[str, SplitManifest]


@dataclass(slots=True)
class LocalDataset:
    name: str
    version: str
    split: str
    root: Path
    recordings: list[Path]
