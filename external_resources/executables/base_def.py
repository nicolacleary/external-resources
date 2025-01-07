import subprocess

from external_resources.executables.type_defs import (
    ExecutablePath,
    ExecutableUseArgs,
    ExecutableUseValue,
)
from external_resources.type_defs import Resource, ExternalResourceUnavailable


class Executable(Resource[ExecutableUseArgs, ExecutableUseValue]):
    executable_path: ExecutablePath
    validation_args: list[str] = ["--version"]

    def _form_args(self, arg_list: list[str]) -> list[str]:
        return [self.executable_path.as_str, *arg_list]

    @property
    def _full_validation_args(self) -> list[str]:
        return self._form_args(self.validation_args)

    def throw_if_unavailable(self) -> None:
        """
        Default implementation checks --version return code is 0
        """
        try:
            validation_args = self._full_validation_args
        except ValueError as err:
            raise ExternalResourceUnavailable(str(err))
        result = subprocess.run(
            args=validation_args,
            capture_output=True,
            text=True,
            check=True,
        )
        if result.returncode != 0:
            raise ExternalResourceUnavailable(f"{validation_args} gave return_code={result.returncode}")
        return None

    def _use(self, args: ExecutableUseArgs) -> ExecutableUseValue:
        """
        Default implementation runs the command once and returns output as text
        Essentially a thin wrapper around subprocess
        """
        result = subprocess.run(
            args=self._form_args(arg_list=args.args),
            capture_output=True,
            text=True,
        )
        return ExecutableUseValue(return_code=result.returncode, stdout=result.stdout, stderr=result.stderr)
