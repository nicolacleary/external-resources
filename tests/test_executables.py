from pathlib import Path

import pytest

from external_resources.executables import (
    Executable,
    executable_type_defs,
    GitExecutable,
)
from external_resources.type_defs import ExternalResourceUnavailable


class SomeNonExistantExecutable(Executable):
    executable_path = executable_type_defs.ExecutablePath(Path("i/do/not/exist"))


@pytest.fixture(scope="module")
def some_executable() -> SomeNonExistantExecutable:
    return SomeNonExistantExecutable()


@pytest.fixture(scope="module")
def git_executable() -> GitExecutable:
    return GitExecutable()


class TestNonExistant:
    """
    Tests all the errors for the worst case (executable doesn't exist at all)
    """

    def test_full_validation_args(self, some_executable: SomeNonExistantExecutable) -> None:
        with pytest.raises(ValueError, match="Executable path does not exist: i.do.not.exist"):
            some_executable._full_validation_args

    def test_is_available(self, some_executable: SomeNonExistantExecutable) -> None:
        assert not some_executable.is_available()

    def test_use(self, some_executable: SomeNonExistantExecutable) -> None:
        """
        We should never get into a state where we get a valid response from a reso
        """
        with pytest.raises(
            ExternalResourceUnavailable,
            match="Executable path does not exist: i.do.not.exist",
        ):
            some_executable.use(args=executable_type_defs.ExecutableUseArgs(args=["--blah"]))


class TestGit:
    """
    Used to test the happy path.
    We assume that git is available in the build environment.
    """

    def test_full_validation_args(self, git_executable: GitExecutable) -> None:
        assert git_executable._full_validation_args == ["git", "--version"]

    def test_is_available(self, git_executable: GitExecutable) -> None:
        assert git_executable.is_available()

    def test_use(self, git_executable: GitExecutable) -> None:
        result = git_executable.use(args=executable_type_defs.ExecutableUseArgs(args=["branch"]))
        assert result.return_code == 0
        assert "*" in result.stdout
        assert not result.stderr
