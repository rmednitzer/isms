#!/usr/bin/env python3
"""
Build an audit pack bundle for an external audit engagement.

Produces dist-audit-pack/<audit_type>-<timestamp>/ with:
  - governance/   (all approved policies, SOPs, standards as rendered)
  - soa/          (Statement of Applicability + justifications)
  - risk/         (risk register, treatment plan, acceptance log)
  - evidence/     (recent attestations + manifests within audit window)
  - audits/       (prior audit records if applicable)
  - reviews/      (management review minutes)
  - README.md     (curated index with auditor orientation)

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DIST = REPO_ROOT / "dist-audit-pack"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", required=True, help="stage-1 | stage-2 | surveillance-YYYY | recertification-YYYY")
    args = parser.parse_args()

    stamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")
    out = DIST / f"{args.audit}-{stamp}"
    out.mkdir(parents=True, exist_ok=True)

    print(f"Building audit pack: {args.audit}")
    print(f"Output: {out}")

    # Governance (instance-rendered if available, else template)
    for sub in ["governance", "operations", "users"]:
        src = REPO_ROOT / "instance" / sub
        if not src.is_dir():
            src = REPO_ROOT / "template" / sub if (REPO_ROOT / "template" / sub).is_dir() else None
        if src:
            shutil.copytree(src, out / sub, dirs_exist_ok=True)

    # Evidence (recent; scope decision is manual per audit type)
    ev_src = REPO_ROOT / "instance" / "evidence"
    if ev_src.is_dir():
        shutil.copytree(ev_src, out / "evidence", dirs_exist_ok=True)

    # Framework refs (law snapshots that the ISMS maps to)
    fr_src = REPO_ROOT / "framework-refs"
    if fr_src.is_dir():
        shutil.copytree(fr_src, out / "framework-refs", dirs_exist_ok=True, ignore=shutil.ignore_patterns("*.xml", "*.tar.gz"))

    # Decisions
    dec_src = REPO_ROOT / "docs" / "decisions"
    if dec_src.is_dir():
        shutil.copytree(dec_src, out / "decisions", dirs_exist_ok=True)

    readme = out / "README.md"
    readme.write_text(f"""# Audit pack: {args.audit}

Built: {datetime.now().isoformat()}
Audit type: {args.audit}

## Structure

- governance/       ISMS scope, policies, procedures, standards, SoA, risk, controls
- operations/       incidents, changes, audits (prior), exercises, reviews
- users/            roles, separation of duties, people-to-role bindings
- evidence/         attestations, manifests, signed PDFs
- framework-refs/   law snapshots and crosswalks
- decisions/        architectural decision records

## Audit orientation

Start at governance/context/scope-statement.md for the ISMS scope.
Then governance/soa/soa.yaml for the Statement of Applicability.
Then governance/risk/register.yaml for the risk register.
Evidence traces from SoA to evidence/ via controls/evidence-plan.yaml.

## Integrity

All commits signed; see .gitsigners and CODEOWNERS at repo root.
QES-signed PDFs under evidence/signatures/; verify via EU DSS.
""", encoding="utf-8")

    print(f"Audit pack built at {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
