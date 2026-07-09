"""Tests for cross-reference validator logic."""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tooling" / "validators"))

from validate_crossrefs import _check_framework_ref, build_catalogue, extract_refs  # noqa: E402


class TestBuildCatalogue:
    def test_catalogue_has_expected_prefixes(self) -> None:
        cat = build_catalogue()
        expected = {"iso27001", "iso27002", "nisg2026", "implreg-2024-2690", "gdpr", "eidas", "nis2"}
        assert expected == set(cat.keys())

    def test_structural_prefixes_accept_any_id(self) -> None:
        from validate_crossrefs import STRUCTURAL_PREFIXES
        assert "eidas" in STRUCTURAL_PREFIXES
        assert "nis2" in STRUCTURAL_PREFIXES
        # iso27001 is no longer a blanket structural prefix: its Annex A refs
        # are now verified against the catalogue.
        assert "iso27001" not in STRUCTURAL_PREFIXES

    def test_iso27001_annex_a_ref_is_validated(self) -> None:
        cat = build_catalogue()
        # A real Annex A control and an ISO management-system clause both pass;
        # a bogus Annex A id is rejected.
        assert _check_framework_ref(Path("x"), "iso27001:A.5.1", cat) is None
        assert _check_framework_ref(Path("x"), "iso27001:6.1.2", cat) is None
        assert _check_framework_ref(Path("x"), "iso27001:A.9.99", cat) is not None


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
