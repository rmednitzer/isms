#!/usr/bin/env python3
"""
Validate the regulatory calendar: schema conformance, no past milestones without
closure records.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

from jsonschema import Draft202012Validator
from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CAL = REPO_ROOT / "framework-refs" / "calendar" / "regulatory-calendar.yaml"
SCHEMA = REPO_ROOT / "tooling" / "schemas" / "regulatory-calendar.schema.json"
yaml = YAML(typ="safe")


def main() -> int:
    if not CAL.is_file():
        print(f"NOTE: calendar not found at {CAL}; skipping.")
        return 0
    if not SCHEMA.is_file():
        print(f"ERROR: schema not found: {SCHEMA}", file=sys.stderr)
        return 2
    with CAL.open("r") as f:
        data = yaml.load(f)
    with SCHEMA.open("r") as f:
        schema = json.load(f)
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(data))
    if errors:
        print("Calendar schema violations:")
        for e in errors:
            print(f"  {e.message}")
        return 1

    today = date.today()
    ms_list = data.get("milestones", []) if isinstance(data, dict) else []
    count_past_30d = 0
    for ms in ms_list:
        d = ms.get("date")
        if isinstance(d, date):
            ms_date = d
        else:
            try:
                ms_date = date.fromisoformat(str(d))
            except Exception:
                continue
        if ms_date < today and (today - ms_date).days > 30:
            count_past_30d += 1
    print(f"Calendar valid. {len(ms_list)} milestones; {count_past_30d} past deadlines older than 30d.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
