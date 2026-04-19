"""Tests for config schema validation."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMA_PATH = REPO_ROOT / "tooling" / "schemas" / "config.schema.json"
CONFIG_PATH = REPO_ROOT / "instance" / "config.yaml"

yaml = YAML(typ="safe")


@pytest.fixture
def validator() -> Draft202012Validator:
    with SCHEMA_PATH.open() as f:
        schema = json.load(f)
    return Draft202012Validator(schema)


def _minimal_config() -> dict:
    return {
        "schema_version": 1,
        "entity": {
            "legal_name": "Test GmbH",
            "short_name": "Test",
            "jurisdiction": "at",
        },
        "classification": {},
        "scope": {},
        "roles": {},
        "providers": {},
        "operational": {},
    }


class TestConfigSchema:
    def test_minimal_valid(self, validator: Draft202012Validator) -> None:
        errors = list(validator.iter_errors(_minimal_config()))
        assert errors == []

    def test_missing_entity(self, validator: Draft202012Validator) -> None:
        cfg = _minimal_config()
        del cfg["entity"]
        errors = list(validator.iter_errors(cfg))
        assert len(errors) > 0

    def test_missing_schema_version(self, validator: Draft202012Validator) -> None:
        cfg = _minimal_config()
        del cfg["schema_version"]
        errors = list(validator.iter_errors(cfg))
        assert len(errors) > 0

    def test_wrong_schema_version(self, validator: Draft202012Validator) -> None:
        cfg = _minimal_config()
        cfg["schema_version"] = 2
        errors = list(validator.iter_errors(cfg))
        assert len(errors) > 0

    def test_invalid_jurisdiction(self, validator: Draft202012Validator) -> None:
        cfg = _minimal_config()
        cfg["entity"]["jurisdiction"] = "xx"
        errors = list(validator.iter_errors(cfg))
        assert len(errors) > 0

    def test_valid_jurisdictions(self, validator: Draft202012Validator) -> None:
        for j in ("at", "de", "ch", "li", "eu"):
            cfg = _minimal_config()
            cfg["entity"]["jurisdiction"] = j
            errors = list(validator.iter_errors(cfg))
            assert errors == [], f"jurisdiction={j} should be valid"

    def test_instance_config_validates(self, validator: Draft202012Validator) -> None:
        """The actual instance/config.yaml should pass schema validation."""
        with CONFIG_PATH.open() as f:
            cfg = yaml.load(f)
        errors = list(validator.iter_errors(cfg))
        assert errors == [], f"instance/config.yaml has schema errors: {errors}"
