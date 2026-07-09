"""Tests for the audit-pack builder.

Focus areas:
  - `has_content` treats a bare `.gitkeep` scaffold as empty, so an
    un-instantiated `instance/` must not shadow the populated `template/`.
  - `--audit` is validated so it cannot escape the output directory.
  - end-to-end `main()` against a synthetic repo confirms the template
    fallback and the warning it emits.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tooling" / "packagers"))

import build_audit_pack as bap  # noqa: E402


def test_has_content_empty_dir(tmp_path: Path) -> None:
    assert bap.has_content(tmp_path) is False


def test_has_content_gitkeep_only_is_empty(tmp_path: Path) -> None:
    (tmp_path / ".gitkeep").write_text("", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / ".gitkeep").write_text("", encoding="utf-8")
    assert bap.has_content(tmp_path) is False


def test_has_content_real_file_is_present(tmp_path: Path) -> None:
    (tmp_path / ".gitkeep").write_text("", encoding="utf-8")
    (tmp_path / "policy.md").write_text("real content", encoding="utf-8")
    assert bap.has_content(tmp_path) is True


def test_has_content_missing_dir(tmp_path: Path) -> None:
    assert bap.has_content(tmp_path / "does-not-exist") is False


@pytest.mark.parametrize("bad", ["../evil", "stage/1", "a b", "", "..", "stage;rm"])
def test_audit_arg_pattern_rejects_path_escape(bad: str) -> None:
    assert bap.AUDIT_ARG_PATTERN.match(bad) is None


@pytest.mark.parametrize("good", ["stage-1", "stage-2", "surveillance-2026", "recertification-2027"])
def test_audit_arg_pattern_accepts_valid(good: str) -> None:
    assert bap.AUDIT_ARG_PATTERN.match(good) is not None


def test_main_rejects_bad_audit_arg(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(bap, "DIST", tmp_path / "dist")
    monkeypatch.setattr(sys, "argv", ["build_audit_pack.py", "--audit", "../escape"])
    assert bap.main() == 2
    assert not (tmp_path / "dist").exists()


def _make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    for sub in ["governance", "operations", "users"]:
        (repo / "template" / sub).mkdir(parents=True)
        (repo / "template" / sub / f"{sub}.md").write_text(f"template {sub}", encoding="utf-8")
        (repo / "instance" / sub).mkdir(parents=True)
        (repo / "instance" / sub / ".gitkeep").write_text("", encoding="utf-8")
    return repo


def test_main_falls_back_to_template_when_instance_is_scaffold(monkeypatch, tmp_path, capsys) -> None:
    repo = _make_repo(tmp_path)
    monkeypatch.setattr(bap, "REPO_ROOT", repo)
    monkeypatch.setattr(bap, "DIST", repo / "dist-audit-pack")
    monkeypatch.setattr(sys, "argv", ["build_audit_pack.py", "--audit", "stage-1"])

    assert bap.main() == 0

    out_dirs = list((repo / "dist-audit-pack").glob("stage-1-*"))
    assert len(out_dirs) == 1
    out = out_dirs[0]
    # Template content was packaged, not the empty instance scaffold.
    assert (out / "governance" / "governance.md").read_text(encoding="utf-8") == "template governance"
    captured = capsys.readouterr()
    assert "empty scaffold" in captured.err
    assert "make instantiate" in captured.err


def test_main_prefers_instance_when_populated(monkeypatch, tmp_path) -> None:
    repo = _make_repo(tmp_path)
    (repo / "instance" / "governance" / "real.md").write_text("instance governance", encoding="utf-8")
    monkeypatch.setattr(bap, "REPO_ROOT", repo)
    monkeypatch.setattr(bap, "DIST", repo / "dist-audit-pack")
    monkeypatch.setattr(sys, "argv", ["build_audit_pack.py", "--audit", "stage-1"])

    assert bap.main() == 0
    out = next((repo / "dist-audit-pack").glob("stage-1-*"))
    assert (out / "governance" / "real.md").read_text(encoding="utf-8") == "instance governance"
    # instance/governance had content, so template governance.md is not present.
    assert not (out / "governance" / "governance.md").exists()
