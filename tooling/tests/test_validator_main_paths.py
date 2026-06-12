"""Exercise the validator main() entry points (finding Q-001).

The existing validator tests cover helper functions but not the main() file-walk
and exit-code paths, which are the actual governance gates CI relies on. These
tests drive each main() against a fixture tree (monkeypatching the scan roots) so
both the pass (exit 0) and violation (exit 1) branches are covered, plus a
happy-path run against the real repository.
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tooling" / "validators"))

import validate_bilingual  # noqa: E402
import validate_crossrefs  # noqa: E402
import validate_frontmatter  # noqa: E402
import validate_supersession  # noqa: E402

VALID_POLICY_FM = textwrap.dedent("""\
    ---
    doc_id: P-900
    doc_type: policy
    title: Fixture policy
    revision: 1
    status: draft
    approved_date: null
    approved_by: null
    owner: role:CISO
    classification: internal
    supersedes_revision: null
    next_review: 2027-01-01
    language: en
    framework_refs:
      - iso27001:5.2
    signature_ref: null
    ---

    Body.
    """)


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


# --- validate_frontmatter -------------------------------------------------

def test_frontmatter_main_passes_on_valid_tree(tmp_path, monkeypatch, capsys) -> None:
    _write(tmp_path / "p-900.md", VALID_POLICY_FM)
    monkeypatch.setattr(validate_frontmatter, "GOVERNANCE_SCAN_ROOTS", (tmp_path,))
    assert validate_frontmatter.main() == 0
    assert "All front-matter valid." in capsys.readouterr().out


def test_frontmatter_main_fails_on_missing_frontmatter(tmp_path, monkeypatch) -> None:
    _write(tmp_path / "no-fm.md", "# Just a heading\n\nNo front-matter.\n")
    monkeypatch.setattr(validate_frontmatter, "GOVERNANCE_SCAN_ROOTS", (tmp_path,))
    assert validate_frontmatter.main() == 1


def test_frontmatter_main_passes_on_real_repo() -> None:
    assert validate_frontmatter.main() == 0


# --- validate_supersession ------------------------------------------------

def _supersession_doc(doc_id: str, revision: int, status: str) -> str:
    return textwrap.dedent(f"""\
        ---
        doc_id: {doc_id}
        revision: {revision}
        status: {status}
        ---

        Body.
        """)


def test_supersession_main_passes_when_one_active(tmp_path, monkeypatch) -> None:
    _write(tmp_path / "r1.md", _supersession_doc("P-901", 1, "superseded"))
    _write(tmp_path / "r2.md", _supersession_doc("P-901", 2, "approved"))
    monkeypatch.setattr(validate_supersession, "SCAN_ROOTS", [tmp_path])
    assert validate_supersession.main() == 0


def test_supersession_main_fails_on_multiple_active(tmp_path, monkeypatch, capsys) -> None:
    _write(tmp_path / "r1.md", _supersession_doc("P-901", 1, "draft"))
    _write(tmp_path / "r2.md", _supersession_doc("P-901", 2, "draft"))
    monkeypatch.setattr(validate_supersession, "SCAN_ROOTS", [tmp_path])
    assert validate_supersession.main() == 1
    assert "multiple active revisions" in capsys.readouterr().out


# --- validate_bilingual ---------------------------------------------------

def _bilingual_doc(lang: str) -> str:
    return textwrap.dedent(f"""\
        ---
        doc_id: P-902
        language: {lang}
        bilingual: true
        ---

        Body.
        """)


def test_bilingual_main_passes_when_companion_present(tmp_path, monkeypatch) -> None:
    _write(tmp_path / "bi.en.md", _bilingual_doc("en"))
    _write(tmp_path / "bi.de.md", _bilingual_doc("de"))
    monkeypatch.setattr(validate_bilingual, "GOVERNANCE_SCAN_ROOTS", (tmp_path,))
    assert validate_bilingual.main() == 0


def test_bilingual_main_fails_when_companion_missing(tmp_path, monkeypatch) -> None:
    _write(tmp_path / "bi.en.md", _bilingual_doc("en"))
    monkeypatch.setattr(validate_bilingual, "GOVERNANCE_SCAN_ROOTS", (tmp_path,))
    assert validate_bilingual.main() == 1


# --- validate_crossrefs ---------------------------------------------------

def test_crossrefs_main_passes_on_real_repo() -> None:
    assert validate_crossrefs.main() == 0
