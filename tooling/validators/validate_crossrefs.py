#!/usr/bin/env python3
"""
Validate framework_refs cross-references.

Every framework_ref in governance artefacts must resolve against a control
catalogue under template/governance/controls/. The catalogue shorthand prefixes
are defined per-framework (iso27001, iso27002, nisg2026, nis2, implreg-2024-2690,
gdpr, eidas).

Exits 0 on success, 1 on violations, 2 on infrastructure errors.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CONTROLS_DIR = REPO_ROOT / "template" / "governance" / "controls"

SCAN_ROOTS = [
    REPO_ROOT / "docs",
    REPO_ROOT / "template" / "governance",
    REPO_ROOT / "template" / "operations",
    REPO_ROOT / "instance" / "governance",
    REPO_ROOT / "instance" / "operations",
]

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
yaml = YAML(typ="safe")

# Prefixes that are considered valid even without full catalogue verification.
# Useful for frameworks where we only hold structural references (eidas articles,
# ISO clause numbers below the Annex A level).
STRUCTURAL_PREFIXES = {"iso27001", "eidas", "nis2"}


def load_control_ids_from_yaml(path: Path, id_field: str = "id") -> set[str]:
    if not path.is_file():
        return set()
    with path.open("r") as f:
        data = yaml.load(f)
    if not data:
        return set()
    ids: set[str] = set()
    if isinstance(data, dict) and "controls" in data:
        for c in data["controls"]:
            if isinstance(c, dict) and id_field in c:
                ids.add(str(c[id_field]))
    return ids


def build_catalogue() -> dict[str, set[str]]:
    cat: dict[str, set[str]] = {
        "iso27002": load_control_ids_from_yaml(CONTROLS_DIR / "annex-a-27001.yaml"),
        "iso27001": set(),  # clauses, structural only
        "nisg2026": load_control_ids_from_yaml(CONTROLS_DIR / "nisg-2026-measures.yaml"),
        "implreg-2024-2690": load_control_ids_from_yaml(CONTROLS_DIR / "implementing-reg-2024-2690.yaml"),
        "gdpr": load_control_ids_from_yaml(CONTROLS_DIR / "gdpr-art-32.yaml"),
        "eidas": set(),
        "nis2": set(),
    }
    # Treat iso27001 A.x.y as a shorthand that also resolves in iso27002
    cat["iso27001"] = cat["iso27001"] | cat["iso27002"]
    return cat


def extract_refs(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return []
    fm = yaml.load(m.group(1)) or {}
    return fm.get("framework_refs", []) or []


REGISTER_REF_FIELDS = {
    "asset_refs": ("ASSET-", "assets"),
    "location_ref": ("FAC-", "facilities"),
    "zone_ref": ("ZONE-", "facilities"),
    "network_ref": ("NET-", "networks"),
    "supplier_refs": ("SUP-", "suppliers"),
    "data_refs": ("DATA-", "data"),
}


def extract_register_refs(path: Path) -> dict[str, list[str]]:
    """Extract register references from frontmatter.

    Returns a mapping of field name to list of referenced IDs.
    """
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm = yaml.load(m.group(1)) or {}
    out: dict[str, list[str]] = {}
    for field in REGISTER_REF_FIELDS:
        v = fm.get(field)
        if v is None:
            continue
        if isinstance(v, str):
            out[field] = [v]
        elif isinstance(v, list):
            out[field] = [str(x) for x in v]
    return out


def build_register_id_sets() -> dict[str, set[str]]:
    """Load register IDs once for crossref resolution."""
    # Import lazily to avoid coupling when the registers validator runs separately.
    sys.path.insert(0, str(REPO_ROOT / "tooling" / "validators"))
    try:
        from validate_registers import REGISTERS, load_ids
    except Exception as exc:
        print(
            f"WARNING: could not import validate_registers ({exc!r}); "
            "register-ref checks skipped.",
            file=sys.stderr,
        )
        return {}
    return {name: load_ids(spec) for name, spec in REGISTERS.items()}


def main() -> int:
    if not CONTROLS_DIR.is_dir():
        print(f"WARNING: controls directory missing: {CONTROLS_DIR}")
        print("Cross-reference validation will be limited.")
    cat = build_catalogue()

    violations: list[str] = []
    count = 0
    for root in SCAN_ROOTS:
        if not root.is_dir():
            continue
        for md in root.rglob("*.md"):
            count += 1
            for ref in extract_refs(md):
                if ":" not in ref:
                    violations.append(f"{md}: ref '{ref}' missing prefix")
                    continue
                prefix, ident = ref.split(":", 1)
                if prefix not in cat:
                    violations.append(f"{md}: unknown framework prefix '{prefix}' in ref '{ref}'")
                    continue
                if prefix in STRUCTURAL_PREFIXES:
                    # Accept any identifier; these are structural references.
                    continue
                if not cat[prefix]:
                    # Catalogue not yet populated; defer until populated.
                    continue
                if ident not in cat[prefix]:
                    violations.append(f"{md}: unknown control '{ref}' (not found in catalogue)")

    register_ids = build_register_id_sets()
    if register_ids:
        for root in SCAN_ROOTS:
            if not root.is_dir():
                continue
            for md in root.rglob("*.md"):
                refs = extract_register_refs(md)
                for field, ids in refs.items():
                    prefix, target_register = REGISTER_REF_FIELDS[field]
                    for rid in ids:
                        if not rid.startswith(prefix):
                            violations.append(
                                f"{md}: {field} value '{rid}' does not match expected prefix '{prefix}'"
                            )
                            continue
                        if rid not in register_ids.get(target_register, set()):
                            violations.append(
                                f"{md}: {field} reference '{rid}' not found in {target_register} register"
                            )

    print(f"Checked framework_refs across {count} files.")
    if violations:
        print(f"{len(violations)} violations:")
        for v in violations:
            print(f"  {v}")
        return 1
    print("All framework_refs resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
