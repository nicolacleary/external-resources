from typing import Type, cast

from external_resources.resource_managers.type_defs import StaticManager, V
from external_resources.type_defs import Resource


def validate_resources_on_declaration(cls: Type[StaticManager[V]]) -> Type[StaticManager[V]]:
    cls.raise_if_any_resource_is_unavailable()
    return cls


class ResourceManager(StaticManager[V]):
    @classmethod
    def _resource_dict(cls) -> dict[str, V]:
        return {
            attribute_name: cast(V, attribute_value)
            for attribute_name, attribute_value in cls.__dict__.items()
            if not attribute_name.startswith("_") and isinstance(attribute_value, Resource)
        }


class CombinedResourceManager(ResourceManager[V]):
    @classmethod
    def _resource_managers(cls) -> dict[str, Type[ResourceManager[V]]]:
        return {
            attribute_name: attribute_value
            for attribute_name, attribute_value in cls.__dict__.items()
            if not attribute_name.startswith("_")
        }

    @classmethod
    def _resource_dict(cls) -> dict[str, V]:
        return {
            resource_name: resource
            for manager in cls._resource_managers().values()
            for resource_name, resource in manager._resource_dict().items()
        }
