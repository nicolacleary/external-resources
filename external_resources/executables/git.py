from pathlib import Path

from external_resources.executables.base_def import Executable
from external_resources.executables.type_defs import ExecutablePath


class GitExecutable(Executable):
    executable_path: ExecutablePath = ExecutablePath(raw_path=Path("git"), skip_exists_check=True)
