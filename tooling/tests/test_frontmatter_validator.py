"""Tests for YAML front-matter validator logic."""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMA_PATH = REPO_ROOT / "tooling" / "schemas" / "frontmatter.schema.json"


@pytest.fixture
def validator() -> Draft202012Validator:
    with SCHEMA_PATH.open() as f:
        schema = json.load(f)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def _make_frontmatter(overrides: dict | None = None) -> dict:
    base = {
        "doc_id": "P-999",
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
    if overrides:
        base.update(overrides)
    return base


class TestFrontmatterSchema:
    def test_valid_draft(self, validator: Draft202012Validator) -> None:
        errors = list(validator.iter_errors(_make_frontmatter()))
        assert errors == []

    def test_missing_doc_id(self, validator: Draft202012Validator) -> None:
        fm = _make_frontmatter()
        del fm["doc_id"]
        errors = list(validator.iter_errors(fm))
        assert len(errors) > 0

    def test_missing_title(self, validator: Draft202012Validator) -> None:
        fm = _make_frontmatter()
        del fm["title"]
        errors = list(validator.iter_errors(fm))
        assert len(errors) > 0

    def test_invalid_status(self, validator: Draft202012Validator) -> None:
        fm = _make_frontmatter({"status": "invalid_status"})
        errors = list(validator.iter_errors(fm))
        assert len(errors) > 0

    def test_revision_must_be_integer(self, validator: Draft202012Validator) -> None:
        fm = _make_frontmatter({"revision": "one"})
        errors = list(validator.iter_errors(fm))
        assert len(errors) > 0

    def test_approved_requires_date_and_approver(self, validator: Draft202012Validator) -> None:
        fm = _make_frontmatter({"status": "approved"})
        errors = list(validator.iter_errors(fm))
        assert len(errors) > 0

    def test_approved_with_date_and_approver(self, validator: Draft202012Validator) -> None:
        fm = _make_frontmatter({
            "status": "approved",
            "approved_date": "2026-04-01",
            "approved_by": "person:ciso",
        })
        errors = list(validator.iter_errors(fm))
        assert errors == []

    def test_valid_procedure_type(self, validator: Draft202012Validator) -> None:
        fm = _make_frontmatter({"doc_type": "procedure", "doc_id": "SOP-001"})
        errors = list(validator.iter_errors(fm))
        assert errors == []

    def test_valid_standard_type(self, validator: Draft202012Validator) -> None:
        fm = _make_frontmatter({"doc_type": "standard", "doc_id": "STD-001"})
        errors = list(validator.iter_errors(fm))
        assert errors == []


class TestFrontmatterExtraction:
    """Test the extract_frontmatter helper from the validator."""

    def test_extract_valid_frontmatter(self, tmp_path: Path) -> None:
        import sys
        sys.path.insert(0, str(REPO_ROOT / "tooling" / "validators"))
        from validate_frontmatter import extract_frontmatter

        md = tmp_path / "test.md"
        md.write_text(textwrap.dedent("""\
            ---
            doc_id: P-001
            title: Test
            ---
            Body text here.
        """))
        result = extract_frontmatter(md)
        assert result is not None
        assert result["doc_id"] == "P-001"

    def test_extract_no_frontmatter(self, tmp_path: Path) -> None:
        import sys
        sys.path.insert(0, str(REPO_ROOT / "tooling" / "validators"))
        from validate_frontmatter import extract_frontmatter

        md = tmp_path / "test.md"
        md.write_text("# Just a heading\n\nNo front-matter here.\n")
        result = extract_frontmatter(md)
        assert result is None
