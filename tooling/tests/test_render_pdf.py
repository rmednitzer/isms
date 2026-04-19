"""Tests for the governance PDF renderer.

The tests cover HTML emission only: WeasyPrint is an optional runtime
dependency and the CI baseline does not ship cairo and pango. PDF emission
is exercised manually via `make pdf DOC=...` on developer machines.
"""
from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tooling" / "packagers"))

from render_pdf import (  # noqa: E402
    RenderError,
    main,
    markdown_to_html,
    normalize_frontmatter,
    parse_document,
    render_html,
)

DOC_CONTROL = REPO_ROOT / "docs" / "document-control.md"
POLICY_SAMPLE = REPO_ROOT / "template" / "governance" / "policy" / "P-000-information-security-policy.md"
STANDARD_SAMPLE = REPO_ROOT / "template" / "governance" / "standards" / "STD-001-password-standard.md"

FIXED_TIME = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)


def test_parse_document_extracts_frontmatter_and_body() -> None:
    doc = parse_document(DOC_CONTROL)
    assert doc.front_matter["doc_id"] == "DOC-001"
    assert doc.front_matter["doc_type"] == "standard"
    assert "# Document control specification" in doc.body_md


def test_parse_document_rejects_missing_frontmatter(tmp_path: Path) -> None:
    bad = tmp_path / "bad.md"
    bad.write_text("# No front-matter here\n", encoding="utf-8")
    with pytest.raises(RenderError):
        parse_document(bad)


def test_normalize_frontmatter_fills_optional_fields() -> None:
    fm = {"doc_id": "P-001", "doc_type": "policy", "title": "x", "revision": 1,
          "status": "draft", "owner": "role:CISO", "classification": "internal",
          "next_review": "2027-01-01", "language": "en", "framework_refs": []}
    out = normalize_frontmatter(fm)
    assert out["interim_signature"] is False
    assert out["signature_ref"] is None
    assert out["supersedes_revision"] is None


def test_markdown_to_html_emits_headings_and_tables() -> None:
    html = markdown_to_html("## Section\n\n| A | B |\n|---|---|\n| 1 | 2 |\n")
    assert "<h2" in html and ">Section</h2>" in html
    assert "<table>" in html
    assert "<td>1</td>" in html or "<td>1 </td>" in html


def test_render_html_for_policy_includes_signature_block() -> None:
    doc = parse_document(POLICY_SAMPLE)
    html = render_html(
        doc,
        entity_legal_name="Example Organisation GmbH",
        emit_signature_block=None,
        generated_at=FIXED_TIME,
    )
    assert 'class="signature-block"' in html
    assert "P-000" in html
    assert "Information Security Policy" in html


def test_render_html_for_standard_omits_signature_block_by_default() -> None:
    doc = parse_document(STANDARD_SAMPLE)
    html = render_html(
        doc,
        entity_legal_name=None,
        emit_signature_block=None,
        generated_at=FIXED_TIME,
    )
    assert 'class="signature-block"' not in html
    assert "STD-001" in html


def test_render_html_for_draft_includes_draft_watermark() -> None:
    doc = parse_document(DOC_CONTROL)
    html = render_html(
        doc,
        entity_legal_name=None,
        emit_signature_block=False,
        generated_at=FIXED_TIME,
    )
    assert "draft-watermark" in html
    assert "DRAFT" in html


def test_cli_html_only_writes_output(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    out = tmp_path / "policy.html"
    rc = main([
        str(POLICY_SAMPLE),
        "--html-only",
        "--out", str(out),
        "--generated-at", "2026-04-19T12:00:00Z",
    ])
    assert rc == 0
    assert out.is_file()
    body = out.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in body
    assert "P-000" in body
