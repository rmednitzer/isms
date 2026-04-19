"""Tests for cross-reference validator logic."""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tooling" / "validators"))

from validate_crossrefs import build_catalogue, extract_refs  # noqa: E402


class TestBuildCatalogue:
    def test_catalogue_has_expected_prefixes(self) -> None:
        cat = build_catalogue()
        expected = {"iso27001", "iso27002", "nisg2026", "implreg-2024-2690", "gdpr", "eidas", "nis2"}
        assert expected == set(cat.keys())

    def test_structural_prefixes_accept_any_id(self) -> None:
        from validate_crossrefs import STRUCTURAL_PREFIXES
        assert "iso27001" in STRUCTURAL_PREFIXES
        assert "eidas" in STRUCTURAL_PREFIXES
        assert "nis2" in STRUCTURAL_PREFIXES


class TestExtractRefs:
    def test_extract_refs_from_frontmatter(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text(
            "---\nframework_refs:\n  - iso27001:5.2\n  - gdpr:Art.32\n---\nBody\n"
        )
        refs = extract_refs(md)
        assert refs == ["iso27001:5.2", "gdpr:Art.32"]

    def test_extract_refs_no_frontmatter(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("# Heading\n\nNo front-matter.\n")
        refs = extract_refs(md)
        assert refs == []

    def test_extract_refs_empty_list(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("---\nframework_refs: []\n---\nBody\n")
        refs = extract_refs(md)
        assert refs == []

    def test_extract_refs_null(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("---\nframework_refs:\n---\nBody\n")
        refs = extract_refs(md)
        assert refs == []
