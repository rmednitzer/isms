"""Basic tests: every schema loads as valid Draft 2020-12 JSON Schema."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMAS_DIR = REPO_ROOT / "tooling" / "schemas"


@pytest.mark.parametrize("schema_file", sorted(SCHEMAS_DIR.glob("*.schema.json")))
def test_schema_loads(schema_file: Path) -> None:
    with schema_file.open() as f:
        schema = json.load(f)
    Draft202012Validator.check_schema(schema)


def test_frontmatter_minimal_example() -> None:
    with (SCHEMAS_DIR / "frontmatter.schema.json").open() as f:
        schema = json.load(f)
    validator = Draft202012Validator(schema)
    sample = {
        "doc_id": "P-000",
        "doc_type": "policy",
        "title": "Test policy",
        "revision": 1,
        "status": "draft",
        "approved_date": None,
        "approved_by": None,
        "owner": "role:CISO",
        "classification": "internal",
        "supersedes_revision": None,
        "next_review": "2027-01-01",
        "language": "en",
        "framework_refs": ["iso27001:5.2"],
        "signature_ref": None,
    }
    assert list(validator.iter_errors(sample)) == []


def test_frontmatter_approved_requires_date() -> None:
    with (SCHEMAS_DIR / "frontmatter.schema.json").open() as f:
        schema = json.load(f)
    validator = Draft202012Validator(schema)
    bad = {
        "doc_id": "P-000",
        "doc_type": "policy",
        "title": "Test",
        "revision": 1,
        "status": "approved",
        "owner": "role:CISO",
        "classification": "internal",
        "next_review": "2027-01-01",
        "language": "en",
        "framework_refs": [],
    }
    errors = list(validator.iter_errors(bad))
    assert len(errors) > 0
