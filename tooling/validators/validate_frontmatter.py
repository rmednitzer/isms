#!/usr/bin/env python3
"""
Validate YAML front-matter on every governance markdown file.

Scans docs/, template/governance/, template/operations/, instance/governance/,
instance/operations/ for .md files and validates their front-matter against
tooling/schemas/frontmatter.schema.json.

Exits 0 on success, 1 on violations, 2 on infrastructure errors.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMA_PATH = REPO_ROOT / "tooling" / "schemas" / "frontmatter.schema.json"

SCAN_ROOTS = [
    REPO_ROOT / "docs",
    REPO_ROOT / "template" / "governance",
    REPO_ROOT / "template" / "operations",
    REPO_ROOT / "instance" / "governance",
    REPO_ROOT / "instance" / "operations",
]

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
yaml = YAML(typ="safe")


def _normalise(value):
    """Serialise date and datetime to ISO strings so JSON Schema format=date/date-time matches."""
    import datetime as _dt
    if isinstance(value, _dt.datetime):
        return value.isoformat()
    if isinstance(value, _dt.date):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _normalise(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalise(v) for v in value]
    return value


def extract_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    data = yaml.load(m.group(1))
    return _normalise(data) if data is not None else None


def validate_file(path: Path, validator: Draft202012Validator) -> list[str]:
    fm = extract_frontmatter(path)
    if fm is None:
        return [f"{path}: missing front-matter"]
    errors = list(validator.iter_errors(fm))
    if not errors:
        return []
    return [f"{path}: {e.message} (at {'/'.join(str(p) for p in e.absolute_path)})" for e in errors]


def main() -> int:
    if not SCHEMA_PATH.is_file():
        print(f"ERROR: schema not found: {SCHEMA_PATH}", file=sys.stderr)
        return 2
    with SCHEMA_PATH.open("r") as f:
        schema = json.load(f)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    errors: list[str] = []
    count = 0
    for root in SCAN_ROOTS:
        if not root.is_dir():
            continue
        for md in root.rglob("*.md"):
            count += 1
            errors.extend(validate_file(md, validator))

    print(f"Validated front-matter on {count} markdown files.")
    if errors:
        print(f"{len(errors)} violations:")
        for e in errors:
            print(f"  {e}")
        return 1
    print("All front-matter valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
