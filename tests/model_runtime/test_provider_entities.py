import pytest

from graphon.model_runtime.entities.common_entities import I18nObject
from graphon.model_runtime.entities.model_entities import ModelType
from graphon.model_runtime.entities.provider_entities import (
    ProviderEntity,
    SimpleProviderEntity,
)


@pytest.mark.parametrize("entity_type", [ProviderEntity, SimpleProviderEntity])
def test_provider_remote_model_catalog_defaults_to_false(
    entity_type: type[ProviderEntity] | type[SimpleProviderEntity],
) -> None:
    provider = entity_type.model_validate({
        "provider": "test-provider",
        "label": {"en_US": "Test Provider"},
        "supported_model_types": ["llm"],
        "configurate_methods": [],
    })

    assert provider.remote_model_catalog is False
    assert provider.model_dump()["remote_model_catalog"] is False
    field = entity_type.model_json_schema()["properties"]["remote_model_catalog"]
    assert field["type"] == "boolean"
    assert field["default"] is False
    assert "remote_model_catalog" not in entity_type.model_json_schema()["required"]


@pytest.mark.parametrize("entity_type", [ProviderEntity, SimpleProviderEntity])
@pytest.mark.parametrize("remote_model_catalog", [False, True])
def test_provider_remote_model_catalog_survives_json_roundtrip(
    entity_type: type[ProviderEntity] | type[SimpleProviderEntity],
    remote_model_catalog: bool,
) -> None:
    provider = entity_type.model_validate({
        "provider": "test-provider",
        "label": {"en_US": "Test Provider"},
        "supported_model_types": ["llm"],
        "configurate_methods": [],
        "remote_model_catalog": remote_model_catalog,
    })

    restored = entity_type.model_validate_json(provider.model_dump_json())

    assert restored.remote_model_catalog is remote_model_catalog
    assert restored.model_dump()["remote_model_catalog"] is remote_model_catalog


@pytest.mark.parametrize("remote_model_catalog", [False, True])
def test_to_simple_provider_preserves_remote_model_catalog(
    remote_model_catalog: bool,
) -> None:
    provider = ProviderEntity(
        provider="test-provider",
        label=I18nObject(en_US="Test Provider"),
        supported_model_types=[ModelType.LLM],
        configurate_methods=[],
        remote_model_catalog=remote_model_catalog,
    )

    simple_provider = provider.to_simple_provider()

    assert simple_provider.remote_model_catalog is remote_model_catalog
    assert simple_provider.provider == provider.provider
