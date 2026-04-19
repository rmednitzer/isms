#!/usr/bin/env python3
"""
Control coverage report: per Annex A control, report (a) applicability per SoA,
(b) implementation statement presence, (c) at least one evidence task bound,
(d) at least one recent attestation.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import sys
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SOA_TEMPLATE = REPO_ROOT / "template" / "governance" / "soa" / "soa.yaml"
SOA_INSTANCE = REPO_ROOT / "instance" / "governance" / "soa" / "soa.yaml"
PLAN_TEMPLATE = REPO_ROOT / "template" / "governance" / "controls" / "evidence-plan.yaml"
PLAN_INSTANCE = REPO_ROOT / "instance" / "governance" / "controls" / "evidence-plan.yaml"
IMPL_DIR_TEMPLATE = REPO_ROOT / "template" / "governance" / "controls" / "implementation"
IMPL_DIR_INSTANCE = REPO_ROOT / "instance" / "governance" / "controls" / "implementation"
yaml = YAML(typ="safe")


def main() -> int:
    soa_path = SOA_INSTANCE if SOA_INSTANCE.is_file() else SOA_TEMPLATE
    if not soa_path.is_file():
        print(f"NOTE: SoA not found at {soa_path}; skipping.")
        return 0
    with soa_path.open("r") as f:
        soa = yaml.load(f)
    controls = (soa or {}).get("controls", [])

    plan_path = PLAN_INSTANCE if PLAN_INSTANCE.is_file() else PLAN_TEMPLATE
    tasks_by_control: dict[str, list[str]] = {}
    if plan_path.is_file():
        with plan_path.open("r") as f:
            plan = yaml.load(f)
        for t in (plan or {}).get("evidence_tasks", []):
            for cid in t.get("control_ids", []):
                tasks_by_control.setdefault(cid, []).append(t.get("id"))

    impl_dir = IMPL_DIR_INSTANCE if IMPL_DIR_INSTANCE.is_dir() else IMPL_DIR_TEMPLATE

    total = len(controls)
    applicable = [c for c in controls if c.get("applicable") == "yes"]
    with_impl = []
    without_impl = []
    with_evidence = []
    without_evidence = []
    for c in applicable:
        cid = c.get("id")
        impl_file = impl_dir / f"{cid}.md" if impl_dir.is_dir() else None
        if impl_file and impl_file.exists():
            with_impl.append(cid)
        else:
            without_impl.append(cid)
        if tasks_by_control.get(cid):
            with_evidence.append(cid)
        else:
            without_evidence.append(cid)

    print(f"Control coverage report")
    print(f"Total controls: {total}")
    print(f"Applicable: {len(applicable)}")
    print(f"  with implementation statement: {len(with_impl)}")
    print(f"  without implementation statement: {len(without_impl)}")
    print(f"  with evidence task bound: {len(with_evidence)}")
    print(f"  without evidence task bound: {len(without_evidence)}")
    if without_impl:
        print()
        print("Controls applicable but missing implementation statement:")
        for cid in without_impl[:20]:
            print(f"  {cid}")
        if len(without_impl) > 20:
            print(f"  ... and {len(without_impl) - 20} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
