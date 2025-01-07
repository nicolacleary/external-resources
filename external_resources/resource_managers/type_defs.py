from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from external_resources.type_defs import IsResource


V = TypeVar("V", bound=IsResource)


class StaticManager(Generic[V], metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def _resource_dict(cls) -> dict[str, V]: ...

    @classmethod
    def as_list(cls) -> list[V]:
        return list(cls._resource_dict().values())

    @classmethod
    def raise_if_any_resource_is_unavailable(cls) -> None:
        for resource in cls.as_list():
            resource.throw_if_unavailable()
