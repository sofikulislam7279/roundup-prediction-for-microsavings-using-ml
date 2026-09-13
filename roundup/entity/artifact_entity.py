from dataclasses import dataclass
from typing import Optional


@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str
