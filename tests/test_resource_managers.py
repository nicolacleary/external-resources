import pytest

from pydantic import BaseModel

from external_resources.resource_managers import (
    ResourceManager,
    CombinedResourceManager,
    validate_resources_on_declaration,
)
from external_resources.type_defs import ExternalResourceUnavailable, Resource


UNAVAILABLE_NUMBER = 123
AVAILABLE_NUMBER = 456


class FakeResourceUseArgs(BaseModel):
    value_to_add: int


class FakeResourceUseOutput(BaseModel):
    result: int


class FakeResource(BaseModel, Resource[FakeResourceUseArgs, FakeResourceUseOutput]):
    stored_value: int

    def throw_if_unavailable(self) -> None:
        if self.stored_value == UNAVAILABLE_NUMBER:
            raise ExternalResourceUnavailable("some message")
        return None

    def _use(self, args: FakeResourceUseArgs) -> FakeResourceUseOutput:
        return FakeResourceUseOutput(result=self.stored_value + args.value_to_add)


@pytest.fixture
def available_resource() -> FakeResource:
    return FakeResource(stored_value=AVAILABLE_NUMBER)


@pytest.fixture
def unavailable_resource() -> FakeResource:
    return FakeResource(stored_value=UNAVAILABLE_NUMBER)


def test_fake_resource_works(available_resource: FakeResource, unavailable_resource: FakeResource) -> None:
    """Santity check that fake resource behaves expectely for the tests"""
    use_args = FakeResourceUseArgs(value_to_add=1)
    print(type(available_resource))

    with pytest.raises(ExternalResourceUnavailable, match="some message"):
        unavailable_resource.use(use_args)

    assert available_resource.use(use_args) == FakeResourceUseOutput(result=AVAILABLE_NUMBER + 1)


class TestResourceManager:
    def test_validate_all_resources_available(self, available_resource: FakeResource) -> None:
        @validate_resources_on_declaration
        class AllAvailable(ResourceManager[FakeResource]):
            RESOURCE_A = available_resource

    def test_validate_some_resources_unavailable(self, unavailable_resource: FakeResource) -> None:
        with pytest.raises(ExternalResourceUnavailable, match="some message"):

            @validate_resources_on_declaration
            class SomeResources(ResourceManager[FakeResource]):
                RESOURCE_A = available_resource
                RESOURCE_B = unavailable_resource

    def test_validate_all_resources_unavailable(self, unavailable_resource: FakeResource) -> None:
        with pytest.raises(ExternalResourceUnavailable, match="some message"):

            @validate_resources_on_declaration
            class AllUnavailable(ResourceManager[FakeResource]):
                RESOURCE_A = unavailable_resource

    def test_resource_dict(self, available_resource: FakeResource, unavailable_resource: FakeResource) -> None:
        class SomeResources(ResourceManager[FakeResource]):
            RESOURCE_A = available_resource
            RESOURCE_B = unavailable_resource

        assert SomeResources._resource_dict() == {
            "RESOURCE_A": available_resource,
            "RESOURCE_B": unavailable_resource,
        }

    def test_as_list(self, available_resource: FakeResource, unavailable_resource: FakeResource) -> None:
        class SomeResources(ResourceManager[FakeResource]):
            RESOURCE_A = available_resource
            RESOURCE_B = unavailable_resource

        assert SomeResources.as_list() == [available_resource, unavailable_resource]


class TestCombinedResourceManager:
    def test_resource_managers(self, available_resource: FakeResource, unavailable_resource: FakeResource) -> None:
        class ManagerA(ResourceManager[FakeResource]):
            RESOURCE_A = available_resource

        class ManagerB(ResourceManager[FakeResource]):
            RESOURCE_B = unavailable_resource

        class AllResources(CombinedResourceManager[FakeResource]):
            FOO = ManagerA
            BAR = ManagerB

        assert AllResources._resource_managers() == {
            "FOO": ManagerA,
            "BAR": ManagerB,
        }

    def test_resource_dict(self, available_resource: FakeResource, unavailable_resource: FakeResource) -> None:
        class ManagerA(ResourceManager[FakeResource]):
            RESOURCE_A = available_resource

        class ManagerB(ResourceManager[FakeResource]):
            RESOURCE_B = unavailable_resource

        class AllResources(CombinedResourceManager[FakeResource]):
            FOO = ManagerA
            BAR = ManagerB

        assert AllResources._resource_dict() == {
            "RESOURCE_A": available_resource,
            "RESOURCE_B": unavailable_resource,
        }

    def test_as_list(self, available_resource: FakeResource, unavailable_resource: FakeResource) -> None:
        class ManagerA(ResourceManager[FakeResource]):
            RESOURCE_A = available_resource

        class ManagerB(ResourceManager[FakeResource]):
            RESOURCE_B = unavailable_resource

        class AllResources(CombinedResourceManager[FakeResource]):
            FOO = ManagerA
            BAR = ManagerB

        assert AllResources.as_list() == [available_resource, unavailable_resource]
