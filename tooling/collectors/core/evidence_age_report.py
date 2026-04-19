#!/usr/bin/env python3
"""
Evidence age report: scans the evidence plan, finds latest attestation per
evidence task, reports staleness against configured cadence. Offline.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import sys
from datetime import date, datetime, timezone
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
PLAN_PATH_TEMPLATE = REPO_ROOT / "template" / "governance" / "controls" / "evidence-plan.yaml"
PLAN_PATH_INSTANCE = REPO_ROOT / "instance" / "governance" / "controls" / "evidence-plan.yaml"
EVIDENCE_ROOT = REPO_ROOT / "instance" / "evidence"
yaml = YAML(typ="safe")


def latest_attestation_date(task_id: str) -> date | None:
    if not EVIDENCE_ROOT.is_dir():
        return None
    latest: date | None = None
    for att in EVIDENCE_ROOT.rglob("*.json"):
        try:
            import json
            with att.open("r") as f:
                data = json.load(f)
            if data.get("evidence_task_id") != task_id:
                continue
            collected = data.get("collected_at", "")
            d = datetime.fromisoformat(collected.replace("Z", "+00:00")).date()
            if latest is None or d > latest:
                latest = d
        except Exception:
            continue
    return latest


def main() -> int:
    plan_path = PLAN_PATH_INSTANCE if PLAN_PATH_INSTANCE.is_file() else PLAN_PATH_TEMPLATE
    if not plan_path.is_file():
        print(f"NOTE: evidence plan not found at {plan_path}; skipping.")
        return 0
    with plan_path.open("r") as f:
        plan = yaml.load(f)
    tasks = (plan or {}).get("evidence_tasks", [])
    today = date.today()
    ok, stale, never = [], [], []
    for t in tasks:
        tid = t.get("id")
        cadence = t.get("cadence_days", 90)
        last = latest_attestation_date(tid)
        if last is None:
            never.append(f"{tid} (cadence {cadence}d)")
        elif (today - last).days > cadence:
            stale.append(f"{tid} last {(today - last).days}d ago (cadence {cadence}d)")
        else:
            ok.append(f"{tid} last {(today - last).days}d ago (cadence {cadence}d)")

    print(f"Evidence coverage report - {today.isoformat()}")
    print()
    print(f"OK ({len(ok)} tasks):")
    for s in ok[:30]:
        print(f"  {s}")
    if len(ok) > 30:
        print(f"  ... and {len(ok) - 30} more")
    print()
    if stale:
        print(f"STALE ({len(stale)} tasks):")
        for s in stale:
            print(f"  {s}")
        print()
    if never:
        print(f"NEVER COLLECTED ({len(never)} tasks):")
        for s in never:
            print(f"  {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
