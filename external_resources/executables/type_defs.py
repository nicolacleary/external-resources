from pathlib import Path
from typing import NamedTuple

from pydantic import BaseModel


class ExecutablePath(NamedTuple):
    raw_path: Path
    skip_exists_check: bool = False

    @property
    def as_str(self) -> str:
        if (not self.skip_exists_check) and (not self.raw_path.exists()):
            raise ValueError(f"Executable path does not exist: {self.raw_path}")
        return str(self.raw_path)


class ExecutableUseArgs(BaseModel):
    args: list[str]


class ExecutableUseValue(BaseModel):
    return_code: int
    stdout: str
    stderr: str
