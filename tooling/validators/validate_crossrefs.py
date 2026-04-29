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

import sys
from pathlib import Path

from _common import (
    FRONTMATTER_RE,  # noqa: F401  (re-exported for backwards compatibility with tests)
    GOVERNANCE_SCAN_ROOTS,
    REPO_ROOT,
    iter_markdown,
    parse_frontmatter,
)
from ruamel.yaml import YAML

CONTROLS_DIR = REPO_ROOT / "template" / "governance" / "controls"
SCAN_ROOTS = GOVERNANCE_SCAN_ROOTS

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
    if not data or not isinstance(data, dict):
        return set()
    ids: set[str] = set()
    for c in data.get("controls", []) or []:
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
    """Return the framework_refs declared in a file's front-matter (or [])."""
    fm = parse_frontmatter(path)
    if fm is None:
        return []
    return fm.get("framework_refs", []) or []


REGISTER_REF_FIELDS = {
    "asset_refs": ("ASSET-", "assets"),
    "location_ref": ("FAC-", "facilities"),
    "zone_ref": ("ZONE-", "facilities"),
    "network_ref": ("NET-", "networks"),
    "supplier_refs": ("SUP-", "suppliers"),
    "data_refs": ("DATA-", "data"),
}


def extract_register_refs_from_fm(fm: dict) -> dict[str, list[str]]:
    """Pull declared register references from an already-parsed front-matter dict."""
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


def extract_register_refs(path: Path) -> dict[str, list[str]]:
    """Backwards-compatible wrapper that parses front-matter from a path."""
    fm = parse_frontmatter(path)
    if fm is None:
        return {}
    return extract_register_refs_from_fm(fm)


def build_register_id_sets() -> dict[str, set[str]]:
    """Load register IDs once for crossref resolution."""
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


def _check_framework_ref(md: Path, ref: str, cat: dict[str, set[str]]) -> str | None:
    if ":" not in ref:
        return f"{md}: ref '{ref}' missing prefix"
    prefix, ident = ref.split(":", 1)
    if prefix not in cat:
        return f"{md}: unknown framework prefix '{prefix}' in ref '{ref}'"
    if prefix in STRUCTURAL_PREFIXES:
        return None
    if not cat[prefix]:
        # Catalogue not yet populated; defer until populated.
        return None
    if ident not in cat[prefix]:
        return f"{md}: unknown control '{ref}' (not found in catalogue)"
    return None


def _check_register_refs(
    md: Path,
    refs: dict[str, list[str]],
    register_ids: dict[str, set[str]],
) -> list[str]:
    out: list[str] = []
    for field, ids in refs.items():
        prefix, target_register = REGISTER_REF_FIELDS[field]
        for rid in ids:
            if not rid.startswith(prefix):
                out.append(
                    f"{md}: {field} value '{rid}' does not match expected prefix '{prefix}'"
                )
                continue
            if rid not in register_ids.get(target_register, set()):
                out.append(
                    f"{md}: {field} reference '{rid}' not found in {target_register} register"
                )
    return out


def main() -> int:
    if not CONTROLS_DIR.is_dir():
        print(f"WARNING: controls directory missing: {CONTROLS_DIR}")
        print("Cross-reference validation will be limited.")
    cat = build_catalogue()
    register_ids = build_register_id_sets()

    violations: list[str] = []
    count = 0
    for md in iter_markdown(SCAN_ROOTS):
        count += 1
        fm = parse_frontmatter(md)
        if fm is None:
            continue
        for ref in fm.get("framework_refs", []) or []:
            err = _check_framework_ref(md, ref, cat)
            if err:
                violations.append(err)
        if register_ids:
            violations.extend(
                _check_register_refs(md, extract_register_refs_from_fm(fm), register_ids)
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
