#!/usr/bin/env python3
"""
A.5.9 evidence collector against the asset register.

Replaces inventory_from_repo.py as the A.5.9 binding. Produces an
attestation that enumerates the asset register at a point in time,
with entry counts by class, criticality, and lifecycle status.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
yaml = YAML(typ="safe")

REGISTER_CANDIDATES = [
    REPO_ROOT / "instance" / "governance" / "assets" / "register.yaml",
    REPO_ROOT / "template" / "governance" / "assets" / "register.yaml",
]


def git_rev() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


def load_register() -> tuple[Path | None, list[dict]]:
    for cand in REGISTER_CANDIDATES:
        if cand.is_file():
            with cand.open("r") as f:
                data = yaml.load(f) or {}
            return cand, list(data.get("assets") or [])
    return None, []


def main() -> int:
    now = datetime.now(UTC)
    path, assets = load_register()
    if path is None:
        print(
            json.dumps(
                {
                    "schema_version": 1,
                    "control_id": "A.5.9",
                    "attestation_type": "asset_register_snapshot",
                    "evidence_task_id": "ET-CORE-001",
                    "collected_at": now.isoformat(),
                    "collected_by": "collectors/core/inventory_from_register.py",
                    "collection_method": "automated_test",
                    "source_system": "git",
                    "observations": {
                        "register_found": False,
                        "note": "Asset register not present; create at template/governance/assets/register.yaml",
                    },
                },
                indent=2,
            )
        )
        return 0

    class_counts = Counter(a.get("class", "unknown") for a in assets)
    crit_counts = Counter(a.get("criticality", "unknown") for a in assets)
    life_counts = Counter(a.get("lifecycle_status", "unknown") for a in assets)
    in_scope = sum(1 for a in assets if a.get("in_scope"))

    attestation = {
        "schema_version": 1,
        "control_id": "A.5.9",
        "attestation_type": "asset_register_snapshot",
        "evidence_task_id": "ET-CORE-001",
        "collected_at": now.isoformat(),
        "collected_by": "collectors/core/inventory_from_register.py",
        "collection_method": "automated_test",
        "source_system": "git",
        "observations": {
            "register_path": str(path.relative_to(REPO_ROOT)),
            "git_head": git_rev(),
            "total_assets": len(assets),
            "in_scope_assets": in_scope,
            "by_class": dict(class_counts),
            "by_criticality": dict(crit_counts),
            "by_lifecycle_status": dict(life_counts),
        },
    }
    print(json.dumps(attestation, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
