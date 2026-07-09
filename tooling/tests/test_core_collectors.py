"""Tests for the core (offline) evidence collectors.

These four collectors had no regression protection. The tests exercise the
pure helpers with synthetic inputs and run each ``main()`` against the live
template layer as an integration smoke test.
"""
from __future__ import annotations

import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tooling" / "collectors" / "core"))

import control_coverage  # noqa: E402
import evidence_age_report  # noqa: E402
import inventory_from_register as ifr  # noqa: E402
import inventory_from_repo  # noqa: E402

# --- inventory_from_register (A.5.9) ---

def test_inventory_from_register_counts(monkeypatch, tmp_path, capsys) -> None:
    reg = tmp_path / "register.yaml"
    reg.write_text(
        "assets:\n"
        "  - id: AST-1\n    class: hardware\n    criticality: high\n    lifecycle_status: active\n    in_scope: true\n"
        "  - id: AST-2\n    class: software\n    criticality: low\n    lifecycle_status: active\n    in_scope: false\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(ifr, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(ifr, "REGISTER_CANDIDATES", [reg])
    assert ifr.main() == 0
    out = json.loads(capsys.readouterr().out)
    assert out["control_id"] == "A.5.9"
    assert out["observations"]["total_assets"] == 2
    assert out["observations"]["in_scope_assets"] == 1
    assert out["observations"]["by_class"] == {"hardware": 1, "software": 1}


def test_inventory_from_register_missing_register(monkeypatch, tmp_path, capsys) -> None:
    monkeypatch.setattr(ifr, "REGISTER_CANDIDATES", [tmp_path / "nope.yaml"])
    assert ifr.main() == 0
    out = json.loads(capsys.readouterr().out)
    assert out["observations"]["register_found"] is False


def test_inventory_from_register_emits_schema_valid_attestation(monkeypatch, tmp_path, capsys) -> None:
    """The emitted JSON must satisfy attestation.schema.json."""
    import jsonschema

    schema = json.loads(
        (REPO_ROOT / "tooling" / "schemas" / "attestation.schema.json").read_text(encoding="utf-8")
    )
    reg = tmp_path / "register.yaml"
    reg.write_text("assets: []\n", encoding="utf-8")
    monkeypatch.setattr(ifr, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(ifr, "REGISTER_CANDIDATES", [reg])
    assert ifr.main() == 0
    jsonschema.validate(json.loads(capsys.readouterr().out), schema)


# --- inventory_from_repo (A.5.37) ---

def test_inventory_from_repo_runs_against_live_repo(capsys) -> None:
    assert inventory_from_repo.main() == 0
    out = json.loads(capsys.readouterr().out)
    assert out["control_id"] == "A.5.37"


# --- control_coverage ---

def test_control_coverage_live_template(capsys) -> None:
    assert control_coverage.main() == 0
    report = capsys.readouterr().out
    # The template SoA enumerates all 93 Annex A controls.
    assert "Total controls: 93" in report
    assert "with implementation statement: 93" in report


# --- evidence_age_report ---

def test_latest_attestation_date_picks_newest(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(evidence_age_report, "EVIDENCE_ROOT", tmp_path)
    older = datetime.now(UTC) - timedelta(days=10)
    newer = datetime.now(UTC) - timedelta(days=2)
    for i, ts in enumerate((older, newer)):
        (tmp_path / f"att{i}.json").write_text(
            json.dumps({"evidence_task_id": "ET-CORE-001", "collected_at": ts.isoformat()}),
            encoding="utf-8",
        )
    got = evidence_age_report.latest_attestation_date("ET-CORE-001")
    assert got == newer.date()


def test_latest_attestation_date_none_when_absent(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(evidence_age_report, "EVIDENCE_ROOT", tmp_path)
    assert evidence_age_report.latest_attestation_date("ET-CORE-001") is None


def test_evidence_age_report_runs(capsys) -> None:
    assert evidence_age_report.main() == 0
    assert "Evidence coverage report" in capsys.readouterr().out
