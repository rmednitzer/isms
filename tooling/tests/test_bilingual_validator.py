"""Tests for bilingual validator logic."""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tooling" / "validators"))


class TestBilingualParity:
    def test_bilingual_with_companion(self, tmp_path: Path) -> None:
        en = tmp_path / "doc.en.md"
        de = tmp_path / "doc.de.md"
        en.write_text("---\nbilingual: true\nlanguage: en\n---\nEnglish\n")
        de.write_text("---\nbilingual: true\nlanguage: de\n---\nGerman\n")

        from validate_bilingual import FRONTMATTER_RE, yaml

        text = en.read_text()
        m = FRONTMATTER_RE.match(text)
        assert m is not None
        fm = yaml.load(m.group(1))
        assert fm["bilingual"] is True

        # The companion file should exist
        assert de.is_file()

    def test_bilingual_missing_companion(self, tmp_path: Path) -> None:
        en = tmp_path / "doc.en.md"
        en.write_text("---\nbilingual: true\nlanguage: en\n---\nEnglish only\n")

        # Companion doc.de.md does not exist
        de = tmp_path / "doc.de.md"
        assert not de.is_file()

    def test_non_bilingual_ignored(self, tmp_path: Path) -> None:
        md = tmp_path / "doc.md"
        md.write_text("---\ntitle: Normal doc\n---\nNo bilingual flag\n")

        from validate_bilingual import FRONTMATTER_RE, yaml

        text = md.read_text()
        m = FRONTMATTER_RE.match(text)
        assert m is not None
        fm = yaml.load(m.group(1))
        assert not fm.get("bilingual")
