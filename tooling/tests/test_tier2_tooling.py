"""Tests for the newly implemented Tier 2 tooling:

- build_management_review (ISO 27001 clause 9.3.2 input pack)
- detect_delta (snapshot change classifier)
- the provider evidence collectors (via the shared _provider_common)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tooling" / "packagers"))
sys.path.insert(0, str(REPO_ROOT / "tooling" / "collectors" / "optional"))

import _provider_common as pc  # noqa: E402
import build_management_review as mr  # noqa: E402
import detect_delta as dd  # noqa: E402

ATTESTATION_SCHEMA = json.loads(
    (REPO_ROOT / "tooling" / "schemas" / "attestation.schema.json").read_text(encoding="utf-8")
)


# --- build_management_review ---

def test_management_review_gather_live_repo() -> None:
    data = mr.gather(REPO_ROOT)
    assert data["coverage"]["total"] == 93
    assert data["objectives"], "template ships ISMS objectives"
    assert data["kpis"], "template ships KPI definitions"


def test_management_review_render_has_all_932_sections() -> None:
    data = mr.gather(REPO_ROOT)
    md = mr.render_markdown(data, "2026-H1", "2026-07-09T00:00:00Z", REPO_ROOT)
    for heading in [
        "## a) Status of actions from previous management reviews",
        "## b) Changes in external and internal issues",
        "## c) Changes in needs and expectations of interested parties",
        "## d) Information security performance and effectiveness",
        "## e) Feedback from interested parties",
        "## f) Results of risk assessment and status of the risk treatment plan",
        "## g) Opportunities for continual improvement",
    ]:
        assert heading in md
    # empty risk register is surfaced, not hidden
    assert "Risk register is empty" in md


def test_management_review_main_dry_run(monkeypatch, capsys) -> None:
    monkeypatch.setattr(sys, "argv", ["build_management_review.py", "--period", "2026-H1", "--dry-run"])
    assert mr.main() == 0
    assert "Management review input pack - 2026-H1" in capsys.readouterr().out


def test_management_review_rejects_bad_period(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["build_management_review.py", "--period", "../x", "--dry-run"])
    assert mr.main() == 2


# --- detect_delta ---

def test_visible_text_strips_tags() -> None:
    assert dd.visible_text("<p>Hello  <b>world</b></p>") == "Hello world"


@pytest.mark.parametrize(
    "frac,expected",
    [(0.0, "editorial"), (0.0005, "editorial"), (0.01, "minor"), (0.10, "material"), (0.5, "structural")],
)
def test_classify_delta(frac: float, expected: str) -> None:
    assert dd.classify_delta(frac) == expected


def test_change_fraction_identical_is_zero() -> None:
    assert dd.change_fraction("same text", "same text") == 0.0


def test_change_fraction_detects_change() -> None:
    assert dd.change_fraction("alpha beta gamma", "alpha DELTA gamma") > 0.0


def _write_snapshot(dirpath: Path, version: str, fetched_at: str, html: str, sha: str) -> None:
    dirpath.mkdir(parents=True, exist_ok=True)
    (dirpath / f"{version}.html").write_text(html, encoding="utf-8")
    (dirpath / f"{version}.meta.yaml").write_text(
        "source_id: TEST.SRC\n"
        f"fetched_at: '{fetched_at}'\n"
        f"artifact_files:\n  html:\n    path: {(dirpath / f'{version}.html').relative_to(REPO_ROOT)}\n    sha256: {sha}\n",
        encoding="utf-8",
    )


def test_compare_source_classifies_material(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(dd, "REPO_ROOT", REPO_ROOT)  # artifact paths are repo-relative
    src = REPO_ROOT / "framework-refs" / "snapshots" / "_pytest_tmp_src"
    try:
        _write_snapshot(src, "v1", "2026-01-01T00:00:00Z", "<p>" + "word " * 100 + "</p>", "a" * 64)
        _write_snapshot(src, "v2", "2026-06-01T00:00:00Z", "<p>" + "word " * 50 + "different " * 50 + "</p>", "b" * 64)
        result = dd.compare_source(src)
        assert result is not None
        assert result["source_id"] == "TEST.SRC"
        assert result["classification"] in ("material", "structural")
        assert result["latest"].endswith("v2.html")
    finally:
        for f in src.glob("*"):
            f.unlink()
        src.rmdir()


def test_compare_source_single_version_returns_none(tmp_path) -> None:
    src = tmp_path / "one"
    src.mkdir()
    (src / "v1.meta.yaml").write_text("source_id: X\nfetched_at: '2026-01-01T00:00:00Z'\n", encoding="utf-8")
    assert dd.compare_source(src) is None


# --- provider collectors ---

def test_provider_dry_run_emits_schema_valid_not_collected(capsys) -> None:
    rc = pc.run_collector(
        category="vuln_management",
        control_id="A.8.8",
        attestation_type="vulnerability_state",
        source_system_default="scanner",
        collector_path="tooling/collectors/optional/openvas_vulnerability_state.py",
        argv=["--dry-run"],
    )
    assert rc == 0
    att = json.loads(capsys.readouterr().out)
    jsonschema.validate(att, ATTESTATION_SCHEMA)
    assert att["control_id"] == "A.8.8"
    assert att["observations"]["status"] == "not_collected"
    assert att["collection_method"] == "automated_test"


def test_provider_unconfigured_emits_not_collected(monkeypatch, tmp_path, capsys) -> None:
    cfg = tmp_path / "config.yaml"
    cfg.write_text("providers: {}\n", encoding="utf-8")
    rc = pc.run_collector(
        category="backup",
        control_id="A.8.13",
        attestation_type="backup_attestation",
        source_system_default="backup-provider",
        collector_path="tooling/collectors/optional/veeam_backup_attestation.py",
        argv=["--config", str(cfg)],
    )
    assert rc == 0
    att = json.loads(capsys.readouterr().out)
    jsonschema.validate(att, ATTESTATION_SCHEMA)
    assert att["observations"]["status"] == "not_collected"
    assert "not configured" in att["observations"]["reason"]


def test_load_provider_reads_category(tmp_path) -> None:
    cfg = tmp_path / "config.yaml"
    cfg.write_text("providers:\n  identity:\n    name: keycloak\n    endpoint_env: KC_URL\n", encoding="utf-8")
    prov = pc.load_provider(cfg, "identity")
    assert prov["name"] == "keycloak"
    assert pc.load_provider(cfg, "backup") == {}
