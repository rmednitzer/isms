#!/usr/bin/env python3
"""
Validate the assurance registers: assets, facilities, networks, suppliers,
data inventory. Two passes:

1. Schema conformance: each register validates against its JSON Schema.
2. Cross-register reference resolution: every reference resolves to an
   existing entry in the target register.

Registers checked at instance/ first, template/ fallback.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from _common import REPO_ROOT
from jsonschema import Draft202012Validator, FormatChecker
from ruamel.yaml import YAML

SCHEMAS_DIR = REPO_ROOT / "tooling" / "schemas"

REGISTERS: dict[str, dict] = {
    "assets": {
        "template": REPO_ROOT / "template" / "governance" / "assets" / "register.yaml",
        "instance": REPO_ROOT / "instance" / "governance" / "assets" / "register.yaml",
        "schema": SCHEMAS_DIR / "asset-register.schema.json",
        "collection_key": "assets",
        "id_prefix": "ASSET-",
    },
    "facilities": {
        "template": REPO_ROOT / "template" / "governance" / "assets" / "facilities.yaml",
        "instance": REPO_ROOT / "instance" / "governance" / "assets" / "facilities.yaml",
        "schema": SCHEMAS_DIR / "facilities-register.schema.json",
        "collection_key": "facilities",
        "id_prefix": "FAC-",
    },
    "networks": {
        "template": REPO_ROOT / "template" / "governance" / "assets" / "networks.yaml",
        "instance": REPO_ROOT / "instance" / "governance" / "assets" / "networks.yaml",
        "schema": SCHEMAS_DIR / "network-register.schema.json",
        "collection_key": "segments",
        "id_prefix": "NET-",
    },
    "suppliers": {
        "template": REPO_ROOT / "template" / "governance" / "supply-chain" / "register.yaml",
        "instance": REPO_ROOT / "instance" / "governance" / "supply-chain" / "register.yaml",
        "schema": SCHEMAS_DIR / "supplier-register.schema.json",
        "collection_key": "suppliers",
        "id_prefix": "SUP-",
    },
    "data": {
        "template": REPO_ROOT / "template" / "governance" / "data" / "inventory.yaml",
        "instance": REPO_ROOT / "instance" / "governance" / "data" / "inventory.yaml",
        "schema": SCHEMAS_DIR / "data-inventory.schema.json",
        "collection_key": "processing_activities",
        "id_prefix": "DATA-",
    },
}

yaml = YAML(typ="safe")


def resolve_register_path(spec: dict) -> Path | None:
    if spec["instance"].is_file():
        return spec["instance"]
    if spec["template"].is_file():
        return spec["template"]
    return None


def load_register(path: Path) -> dict:
    with path.open("r") as f:
        data = yaml.load(f)
    return data or {}


def load_ids(spec: dict) -> set[str]:
    path = resolve_register_path(spec)
    if path is None:
        return set()
    data = load_register(path)
    ids: set[str] = set()
    for entry in data.get(spec["collection_key"], []) or []:
        if isinstance(entry, dict) and "id" in entry:
            ids.add(str(entry["id"]))
    # Facilities also contain zones with their own IDs; surface those.
    if spec["id_prefix"] == "FAC-":
        for fac in data.get("facilities", []) or []:
            for zone in (fac.get("zones") or []):
                if isinstance(zone, dict) and "id" in zone:
                    ids.add(str(zone["id"]))
    return ids


def _display_path(p: Path) -> str:
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def validate_schema(name: str, spec: dict) -> list[str]:
    path = resolve_register_path(spec)
    if path is None:
        return [
            f"{name}: register file not found at either "
            f"{_display_path(spec['instance'])} or "
            f"{_display_path(spec['template'])}"
        ]
    with spec["schema"].open("r") as f:
        schema = json.load(f)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    data = load_register(path)
    errors = []
    for err in validator.iter_errors(data):
        loc = "/".join(str(p) for p in err.absolute_path)
        errors.append(f"{name} ({path}): {err.message} [at {loc}]")
    return errors


def validate_crossrefs(all_ids: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []

    # Asset register references
    assets_spec = REGISTERS["assets"]
    path = resolve_register_path(assets_spec)
    if path is not None:
        data = load_register(path)
        for a in data.get("assets", []) or []:
            aid = a.get("id", "<unknown>")
            loc = a.get("location_ref")
            if loc and loc not in all_ids["facilities"]:
                errors.append(f"asset {aid}: location_ref {loc} not found in facilities register")
            zone = a.get("zone_ref")
            if zone and zone not in all_ids["facilities"]:
                # Zones share the facilities namespace in our resolution set.
                errors.append(f"asset {aid}: zone_ref {zone} not found in facilities register")
            net = a.get("network_ref")
            if net and net not in all_ids["networks"]:
                errors.append(f"asset {aid}: network_ref {net} not found in networks register")
            for sup in a.get("supplier_refs", []) or []:
                if sup not in all_ids["suppliers"]:
                    errors.append(f"asset {aid}: supplier_refs entry {sup} not found in suppliers register")
            for dref in a.get("data_refs", []) or []:
                if dref not in all_ids["data"]:
                    errors.append(f"asset {aid}: data_refs entry {dref} not found in data inventory")
            for dep in a.get("dependencies", []) or []:
                if dep not in all_ids["assets"]:
                    errors.append(f"asset {aid}: dependency {dep} not found in asset register")

    # Network register references
    net_spec = REGISTERS["networks"]
    path = resolve_register_path(net_spec)
    if path is not None:
        data = load_register(path)
        for n in data.get("segments", []) or []:
            nid = n.get("id", "<unknown>")
            loc = n.get("location_ref")
            if loc and loc not in all_ids["facilities"]:
                errors.append(f"network {nid}: location_ref {loc} not found in facilities register")
            for peer in n.get("peering", []) or []:
                if peer not in all_ids["networks"]:
                    errors.append(f"network {nid}: peering ref {peer} not found in networks register")

    # Data inventory references
    data_spec = REGISTERS["data"]
    path = resolve_register_path(data_spec)
    if path is not None:
        data = load_register(path)
        for act in data.get("processing_activities", []) or []:
            did = act.get("id", "<unknown>")
            for aref in act.get("asset_refs", []) or []:
                if aref not in all_ids["assets"]:
                    errors.append(f"data {did}: asset_refs entry {aref} not found in asset register")
            for r in act.get("recipients", []) or []:
                if r.get("ref_type") == "supplier":
                    sup = r.get("ref")
                    if sup and sup not in all_ids["suppliers"]:
                        errors.append(f"data {did}: supplier recipient {sup} not found")

    return errors


def main() -> int:
    schema_errors: list[str] = []
    for name, spec in REGISTERS.items():
        schema_errors.extend(validate_schema(name, spec))

    if schema_errors:
        print(f"Register schema violations ({len(schema_errors)}):")
        for e in schema_errors:
            print(f"  {e}")
        return 1

    all_ids = {name: load_ids(spec) for name, spec in REGISTERS.items()}
    print("Register entries loaded:")
    for name, ids in all_ids.items():
        print(f"  {name}: {len(ids)} IDs")

    crossref_errors = validate_crossrefs(all_ids)
    if crossref_errors:
        print(f"Register cross-reference violations ({len(crossref_errors)}):")
        for e in crossref_errors:
            print(f"  {e}")
        return 1

    print("All registers valid and cross-references resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
