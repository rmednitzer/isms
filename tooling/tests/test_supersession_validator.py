"""Tests for supersession chain validator logic."""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tooling" / "validators"))

from validate_supersession import FRONTMATTER_RE, yaml  # noqa: E402


def _write_doc(path: Path, doc_id: str, revision: int, status: str = "draft") -> None:
    path.write_text(textwrap.dedent(f"""\
        ---
        doc_id: {doc_id}
        revision: {revision}
        status: {status}
        ---
        Content for {doc_id} rev {revision}.
    """))


class TestSupersessionParsing:
    def test_single_revision_no_violation(self, tmp_path: Path) -> None:
        _write_doc(tmp_path / "p001.md", "P-001", 1, "draft")
        # Should parse cleanly with one document
        md = tmp_path / "p001.md"
        text = md.read_text()
        m = FRONTMATTER_RE.match(text)
        assert m is not None
        fm = yaml.load(m.group(1))
        assert fm["doc_id"] == "P-001"
        assert fm["revision"] == 1

    def test_superseded_chain(self, tmp_path: Path) -> None:
        _write_doc(tmp_path / "p001v1.md", "P-001", 1, "superseded")
        _write_doc(tmp_path / "p001v2.md", "P-001", 2, "draft")
        # Both should parse; superseded + draft = one active = OK
        for name in ("p001v1.md", "p001v2.md"):
            md = tmp_path / name
            m = FRONTMATTER_RE.match(md.read_text())
            assert m is not None

    def test_multiple_active_detected(self, tmp_path: Path) -> None:
        # Two active revisions of the same doc_id: this is a violation
        _write_doc(tmp_path / "p001v1.md", "P-001", 1, "draft")
        _write_doc(tmp_path / "p001v2.md", "P-001", 2, "approved")
        # Both are non-superseded, so multiple active
        docs = {}
        for name in ("p001v1.md", "p001v2.md"):
            md = tmp_path / name
            m = FRONTMATTER_RE.match(md.read_text())
            fm = yaml.load(m.group(1))
            docs[name] = fm
        active = [d for d in docs.values() if d["status"] not in ("superseded", "retired")]
        assert len(active) == 2  # This would be flagged as a violation
