"""Tests for the PR D tooling fixes."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tooling" / "packagers"))
sys.path.insert(0, str(REPO_ROOT / "tooling" / "collectors" / "optional"))

import _provider_common as pc  # noqa: E402
import build_audit_pack as bap  # noqa: E402
import build_management_review as mr  # noqa: E402
import detect_delta as dd  # noqa: E402

# --- build_audit_pack: symlink refusal (was untested) ---

def test_copytree_refuses_symlink(tmp_path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "real.md").write_text("x", encoding="utf-8")
    (src / "link.md").symlink_to(src / "real.md")
    with pytest.raises(RuntimeError):
        bap.copytree_without_symlinks(src, tmp_path / "dst")


# --- build_audit_pack: certification gate + evidence warning ---

def _repo_with_template_only(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    for sub in ("governance", "operations", "users"):
        (repo / "template" / sub).mkdir(parents=True)
        (repo / "template" / sub / f"{sub}.md").write_text("real", encoding="utf-8")
        (repo / "instance" / sub).mkdir(parents=True)
        (repo / "instance" / sub / ".gitkeep").write_text("", encoding="utf-8")
    (repo / "instance" / "evidence").mkdir(parents=True)
    (repo / "instance" / "evidence" / ".gitkeep").write_text("", encoding="utf-8")
    return repo


def test_audit_pack_stage2_refuses_on_warnings(monkeypatch, tmp_path) -> None:
    repo = _repo_with_template_only(tmp_path)
    monkeypatch.setattr(bap, "REPO_ROOT", repo)
    monkeypatch.setattr(bap, "DIST", repo / "dist")
    monkeypatch.setattr(sys, "argv", ["build_audit_pack.py", "--audit", "stage-2"])
    assert bap.main() == 1


def test_audit_pack_stage1_warns_but_succeeds(monkeypatch, tmp_path, capsys) -> None:
    repo = _repo_with_template_only(tmp_path)
    monkeypatch.setattr(bap, "REPO_ROOT", repo)
    monkeypatch.setattr(bap, "DIST", repo / "dist")
    monkeypatch.setattr(sys, "argv", ["build_audit_pack.py", "--audit", "stage-1"])
    assert bap.main() == 0
    out = next((repo / "dist").glob("stage-1-*"))
    assert "Readiness warnings" in (out / "README.md").read_text(encoding="utf-8")
    assert "evidence/" in capsys.readouterr().err


# --- build_management_review ---

def test_default_period_is_calendar_quarter(monkeypatch) -> None:
    # July -> Q3 (not month %m = Q07)
    import datetime as real_dt

    class FakeDT(real_dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return real_dt.datetime(2026, 7, 9, tzinfo=tz)

    monkeypatch.setattr(mr, "datetime", FakeDT)
    assert mr._default_period() == "2026-Q3"


def test_prefer_ignores_empty_instance(tmp_path) -> None:
    (tmp_path / "instance" / "governance").mkdir(parents=True)
    (tmp_path / "template" / "governance").mkdir(parents=True)
    empty = tmp_path / "instance" / "governance" / "x.yaml"
    empty.write_text("", encoding="utf-8")
    got = mr._prefer(tmp_path, "governance/x.yaml")
    assert got == tmp_path / "template" / "governance" / "x.yaml"


def test_management_review_coverage_numbers() -> None:
    cov = mr.control_coverage(REPO_ROOT)
    assert cov == {"total": 93, "applicable": 93, "assessed": 0, "with_evidence_task": 21}


# --- provider collector: failed pull still emits an attestation ---

def test_provider_failure_emits_collection_failed(monkeypatch, tmp_path, capsys) -> None:
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        "providers:\n  vuln_management:\n    name: openvas\n    endpoint_env: OV_URL\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("OV_URL", "https://example.invalid/api")
    import requests

    def boom(*a, **k):
        raise requests.RequestException("network down")

    monkeypatch.setattr(requests, "get", boom)
    rc = pc.run_collector(
        category="vuln_management",
        control_id="A.8.8",
        attestation_type="vulnerability_state",
        source_system_default="scanner",
        collector_path="x.py",
        argv=["--config", str(cfg)],
    )
    assert rc == 1
    att = json.loads(capsys.readouterr().out)
    assert att["observations"]["status"] == "collection_failed"


# --- detect_delta ordering ---

def test_latest_two_prefers_real_timestamp(tmp_path) -> None:
    d = tmp_path
    (d / "a.meta.yaml").write_text("source_id: X\n", encoding="utf-8")  # no fetched_at
    (d / "b.meta.yaml").write_text("source_id: X\nfetched_at: '2099-01-01T00:00:00Z'\n", encoding="utf-8")
    newest = dd.latest_two(d)[0]
    assert newest[0].name == "b.meta.yaml"


def test_latest_two_version_date_tiebreaker(tmp_path) -> None:
    ts = "fetched_at: '2026-01-01T00:00:00Z'\n"
    (d := tmp_path)
    (d / "a.meta.yaml").write_text(f"source_id: X\n{ts}version_date: '2026-06-01'\n", encoding="utf-8")
    (d / "z.meta.yaml").write_text(f"source_id: X\n{ts}version_date: '2025-01-01'\n", encoding="utf-8")
    # identical fetched_at -> newer version_date wins, not filename order
    assert dd.latest_two(d)[0][0].name == "a.meta.yaml"
