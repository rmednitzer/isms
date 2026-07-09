#!/usr/bin/env python3
"""
Validate the Statement of Applicability for structural integrity.

Enforced (failure):
  - the SoA control set is exactly the Annex A control set (no missing/extra IDs);
  - every applicable control's implementation_ref points at a file that exists;
  - an excluded control (applicable: no) has an exclusion_ref;
  - once a control is assessed (status not in {not_assessed, ''}), it carries a
    justification_ref (ISO/IEC 27001:2022 clause 6.1.3 d)).

This does not force a justification on every control while the SoA is still an
unassessed v1 draft (that gate belongs at audit-pack build time, not on every
commit), but it guarantees that as soon as a control is *assessed* it cannot be
left without the justification the standard requires.

Exits 0 on success, 1 on violations, 2 on infrastructure errors.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import sys
from pathlib import Path

from _common import REPO_ROOT
from ruamel.yaml import YAML

yaml = YAML(typ="safe")

GOV = REPO_ROOT / "template" / "governance"
SOA_INSTANCE = REPO_ROOT / "instance" / "governance" / "soa" / "soa.yaml"
SOA_TEMPLATE = GOV / "soa" / "soa.yaml"
ANNEX = GOV / "controls" / "annex-a-27001.yaml"


def _load(path: Path) -> dict:
    with path.open("r") as f:
        return yaml.load(f) or {}


def main() -> int:
    soa_path = SOA_INSTANCE if SOA_INSTANCE.is_file() else SOA_TEMPLATE
    if not soa_path.is_file():
        print(f"ERROR: SoA not found at {soa_path}", file=sys.stderr)
        return 2
    if not ANNEX.is_file():
        print(f"ERROR: Annex A catalogue not found at {ANNEX}", file=sys.stderr)
        return 2

    soa = _load(soa_path)
    annex = _load(ANNEX)
    controls = soa.get("controls", []) or []
    annex_ids = {str(c["id"]) for c in annex.get("controls", []) if isinstance(c, dict) and "id" in c}
    soa_ids = {str(c["id"]) for c in controls if isinstance(c, dict) and "id" in c}

    violations: list[str] = []

    missing = annex_ids - soa_ids
    extra = soa_ids - annex_ids
    if missing:
        violations.append(f"SoA is missing Annex A controls: {sorted(missing)}")
    if extra:
        violations.append(f"SoA lists non-Annex-A controls: {sorted(extra)}")

    soa_root = soa_path.parent.parent  # governance/
    for c in controls:
        if not isinstance(c, dict):
            continue
        cid = c.get("id", "<no id>")
        applicable = c.get("applicable")
        status = c.get("status") or "not_assessed"
        impl_ref = c.get("implementation_ref")
        just_ref = c.get("justification_ref")
        excl_ref = c.get("exclusion_ref")

        if applicable == "yes":
            if not impl_ref:
                violations.append(f"{cid}: applicable but no implementation_ref")
            elif not (soa_root / impl_ref).is_file():
                violations.append(f"{cid}: implementation_ref does not exist: {impl_ref}")
            if status != "not_assessed" and not just_ref:
                violations.append(
                    f"{cid}: assessed (status={status}) but no justification_ref "
                    "(ISO/IEC 27001:2022 clause 6.1.3 d))"
                )
        elif applicable == "no":
            if not excl_ref:
                violations.append(f"{cid}: excluded (applicable: no) but no exclusion_ref")
        else:
            violations.append(f"{cid}: applicable must be 'yes' or 'no', got {applicable!r}")

    print(f"Checked SoA integrity across {len(controls)} controls ({soa_path.relative_to(REPO_ROOT)}).")
    if violations:
        print(f"{len(violations)} violations:")
        for v in violations:
            print(f"  {v}")
        return 1
    print("SoA structurally consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
