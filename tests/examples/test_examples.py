import pytest
from pathlib import Path


EXAMPLE_FILES = set(Path(__file__).parent.glob("example_*"))
EXAMPLE_NAMES = {file.name.split(".")[0] for file in EXAMPLE_FILES}


@pytest.mark.parametrize("example", EXAMPLE_NAMES)
def test_can_import(example: Path) -> None:
    __import__(f"tests.examples.{example}")
