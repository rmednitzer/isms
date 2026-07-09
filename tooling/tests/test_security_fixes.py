"""Tests for the PR A security and fail-open fixes.

- snapshot fetchers refuse a local_reference that escapes framework-refs/snapshots/
- render_pdf refuses a doc_id that escapes DIST_DIR
- validate_calendar fails on an overdue milestone with no closure record
- structural validators fail closed when they check zero files
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tooling" / "collectors" / "optional"))
sys.path.insert(0, str(REPO_ROOT / "tooling" / "packagers"))
sys.path.insert(0, str(REPO_ROOT / "tooling" / "validators"))

import _snapshot_paths  # noqa: E402
import render_pdf  # noqa: E402

# --- C1: fetcher path containment ---

@pytest.mark.parametrize(
    "ref",
    ["../../../outside", "/etc", "framework-refs/../../../etc", "", None, "framework-refs/sources"],
)
def test_resolve_snapshot_dir_rejects_escape(ref) -> None:
    with pytest.raises(RuntimeError):
        _snapshot_paths.resolve_snapshot_dir(REPO_ROOT, ref)


def test_resolve_snapshot_dir_accepts_inside() -> None:
    got = _snapshot_paths.resolve_snapshot_dir(REPO_ROOT, "framework-refs/snapshots/eu/gdpr/")
    assert got == (REPO_ROOT / "framework-refs" / "snapshots" / "eu" / "gdpr").resolve()


# --- H1: render_pdf output path containment ---

def _doc(doc_id: str):
    return render_pdf.ParsedDoc(
        front_matter={"doc_id": doc_id, "revision": 1},
        body_md="# x",
        source_path=Path("/tmp/x.md"),
    )


def test_default_output_path_neutralizes_traversal() -> None:
    # A traversal doc_id is sanitized to a single component; output stays in DIST_DIR.
    out = render_pdf.default_output_path(_doc("../../../../tmp/escape"), suffix=".html")
    assert out.parent == render_pdf.DIST_DIR.resolve()
    assert ".." not in out.name.split("-R")[0].strip("._")


def test_default_output_path_sanitizes_and_stays_in_dist() -> None:
    out = render_pdf.default_output_path(_doc("P-000"), suffix=".pdf")
    assert out.parent == render_pdf.DIST_DIR.resolve()
    assert out.name.startswith("P-000-R1-")


def test_default_output_path_neutralizes_slashes() -> None:
    out = render_pdf.default_output_path(_doc("a/b/c"), suffix=".html")
    assert out.parent == render_pdf.DIST_DIR.resolve()
    assert "/" not in out.name[:-5]  # no path separators survive into the component


# --- H2: calendar overdue milestone fails ---

def _load_validator(name: str):
    path = REPO_ROOT / "tooling" / "validators" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_calendar_fails_on_overdue_without_closure(tmp_path, capsys) -> None:
    vc = _load_validator("validate_calendar")
    cal = tmp_path / "cal.yaml"
    cal.write_text(
        "schema_version: 1\nmilestones:\n"
        "  - id: MS-2020-001\n    source_id: X\n    event: overdue thing\n    date: '2020-01-01'\n",
        encoding="utf-8",
    )
    vc.CAL = cal
    assert vc.main() == 1
    assert "overdue" in capsys.readouterr().out.lower()


def test_calendar_passes_when_overdue_is_closed(tmp_path) -> None:
    vc = _load_validator("validate_calendar")
    cal = tmp_path / "cal.yaml"
    cal.write_text(
        "schema_version: 1\nmilestones:\n"
        "  - id: MS-2020-001\n    source_id: X\n    event: done thing\n"
        "    date: '2020-01-01'\n    status: closed\n",
        encoding="utf-8",
    )
    vc.CAL = cal
    assert vc.main() == 0


# --- H3: fail-open guard ---

def test_frontmatter_fails_closed_on_zero_files(monkeypatch) -> None:
    vf = _load_validator("validate_frontmatter")
    monkeypatch.setattr(vf, "GOVERNANCE_SCAN_ROOTS", (REPO_ROOT / "does-not-exist",))
    monkeypatch.delenv("ISMS_ALLOW_EMPTY", raising=False)
    assert vf.main() == 2


def test_frontmatter_allow_empty_override(monkeypatch) -> None:
    vf = _load_validator("validate_frontmatter")
    monkeypatch.setattr(vf, "GOVERNANCE_SCAN_ROOTS", (REPO_ROOT / "does-not-exist",))
    monkeypatch.setenv("ISMS_ALLOW_EMPTY", "1")
    assert vf.main() == 0
