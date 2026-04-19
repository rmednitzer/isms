#!/usr/bin/env python3
"""
Inventory everything tracked in the repository that constitutes asset evidence.

For A.5.9 Inventory of information and other associated assets, the repository
itself can be enumerated: governance documents, SOPs, policies, risk register,
SoA, evidence tasks. This attestation captures that enumeration.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def git_rev() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()
    except Exception:
        return "unknown"


def main() -> int:
    now = datetime.now(timezone.utc)
    artefacts = []
    for root_name in ["docs", "template/governance", "instance/governance"]:
        root = REPO_ROOT / root_name
        if not root.is_dir():
            continue
        for md in root.rglob("*.md"):
            rel = md.relative_to(REPO_ROOT)
            artefacts.append(str(rel))

    attestation = {
        "schema_version": 1,
        "control_id": "A.5.9",
        "attestation_type": "repo_inventory",
        "evidence_task_id": "ET-CORE-001",
        "collected_at": now.isoformat(),
        "collected_by": "collectors/core/inventory_from_repo.py",
        "collection_method": "automated_test",
        "source_system": "git",
        "observations": {
            "git_head": git_rev(),
            "artefact_count": len(artefacts),
            "artefacts": sorted(artefacts)[:200],  # cap for manifest brevity
        },
    }
    print(json.dumps(attestation, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
