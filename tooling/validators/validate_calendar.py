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

from _common import REPO_ROOT
from jsonschema import Draft202012Validator, FormatChecker
from ruamel.yaml import YAML

CAL = REPO_ROOT / "framework-refs" / "calendar" / "regulatory-calendar.yaml"
SCHEMA = REPO_ROOT / "tooling" / "schemas" / "regulatory-calendar.schema.json"
yaml = YAML(typ="safe")

PAST_DEADLINE_THRESHOLD_DAYS = 30


def _is_closed(ms: dict) -> bool:
    """A milestone is closed once its obligations are discharged.

    The regulatory-calendar schema allows extra properties, so closure is
    recorded on the milestone itself: either ``status: closed`` or a
    ``closure_ref`` pointing at the record that discharges the obligation.
    """
    if str(ms.get("status", "")).lower() in {"closed", "discharged", "superseded"}:
        return True
    return bool(ms.get("closure_ref"))


def main() -> int:
    if not CAL.is_file():
        print(f"NOTE: calendar not found at {CAL}; skipping.")
        return 0
    if not SCHEMA.is_file():
        print(f"ERROR: schema not found: {SCHEMA}", file=sys.stderr)
        return 2
    with CAL.open("r") as f:
        data = yaml.load(f)
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = list(validator.iter_errors(data))
    if errors:
        print("Calendar schema violations:")
        for e in errors:
            print(f"  {e.message}")
        return 1

    today = date.today()
    ms_list = data.get("milestones", []) if isinstance(data, dict) else []
    overdue: list[str] = []
    bad_dates: list[str] = []
    for ms in ms_list:
        d = ms.get("date")
        if isinstance(d, date):
            ms_date = d
        else:
            try:
                ms_date = date.fromisoformat(str(d))
            except ValueError:
                bad_dates.append(f"{ms.get('id', '<no id>')}: unparseable date {d!r}")
                continue
        if ms_date < today and (today - ms_date).days > PAST_DEADLINE_THRESHOLD_DAYS:
            if not _is_closed(ms):
                overdue.append(
                    f"{ms.get('id', '<no id>')} ({ms.get('event', '?')}): due {ms_date.isoformat()}, "
                    f"{(today - ms_date).days}d overdue with no closure record"
                )
    if bad_dates:
        print(f"Calendar date violations ({len(bad_dates)}):")
        for b in bad_dates:
            print(f"  {b}")
        return 1
    if overdue:
        print(f"Overdue milestones without closure record ({len(overdue)}):")
        for o in overdue:
            print(f"  {o}")
        print(
            "Mark a milestone `status: closed` (or add `closure_ref:`) once its "
            "obligations are discharged, per SOP-102."
        )
        return 1
    print(f"Calendar valid. {len(ms_list)} milestones; no overdue milestones without closure.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
