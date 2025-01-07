from abc import ABCMeta, abstractmethod
from typing import Any, Generic, TypeVar, Protocol

from pydantic import BaseModel
from pydantic.dataclasses import dataclass as pydantic_dataclass


T_UseArgs = TypeVar("T_UseArgs", bound=(BaseModel | None))
V_UseOutput = TypeVar("V_UseOutput", bound=(BaseModel | None))


class ExternalResourceUnavailable(Exception):
    """
    Thrown when evaluating if a resource is available
    """


@pydantic_dataclass
class Resource(Generic[T_UseArgs, V_UseOutput], metaclass=ABCMeta):
    @abstractmethod
    def throw_if_unavailable(self) -> None:
        """
        Each resource should provide a way to check its availability using only its initial definition.
        This is intended to be used at the very start of a program.
        """
        ...

    def is_available(self) -> bool:
        """
        Please see throw_if_unavailable
        """
        try:
            self.throw_if_unavailable()
        except ExternalResourceUnavailable:
            return False
        return True

    @abstractmethod
    def _use(self, args: T_UseArgs) -> V_UseOutput:
        """
        Use a resource.
        The args must be passed in a single object that subclasses pydantic.BaseModel.
        This is intended to be used at any point after the availability has been checked.
        """
        ...

    def use(self, args: T_UseArgs) -> V_UseOutput:
        """
        Please see _use
        """
        self.throw_if_unavailable()
        return self._use(args)


class IsResource(Protocol):
    def throw_if_unavailable(self) -> None: ...

    def use(self, args: Any) -> Any: ...
