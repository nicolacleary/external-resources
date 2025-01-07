import pytest
from pathlib import Path


EXAMPLE_FILES = set(Path(__file__).parent.glob("example_*"))
EXAMPLE_NAMES = {file.name.split(".")[0] for file in EXAMPLE_FILES}


@pytest.mark.parametrize("example", EXAMPLE_NAMES)
def test_can_import(example: Path) -> None:
    __import__(f"tests.examples.{example}")


def test_no_unexpected_files() -> None:
    example_files = {file.name for file in EXAMPLE_FILES}
    all_files = {file.name for file in Path(__file__).parent.glob("*") if not file.name.startswith("__")}
    unexpected_files = all_files - example_files - {Path(__file__).name}

    assert not unexpected_files, f"All test files should be named 'example_*', found: {unexpected_files}"
