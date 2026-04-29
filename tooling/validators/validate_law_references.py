#!/usr/bin/env python3
"""
Validate that every source listed in framework-refs/sources/registry.yaml has a
recent-enough snapshot, per its check_frequency_days configuration.

Reports sources that are stale but does not fail the build by default; use --strict
to fail on staleness.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import sys
from datetime import date, datetime

from _common import REPO_ROOT
from ruamel.yaml import YAML

REGISTRY = REPO_ROOT / "framework-refs" / "sources" / "registry.yaml"
SNAPSHOTS_ROOT = REPO_ROOT / "framework-refs" / "snapshots"
yaml = YAML(typ="safe")


def _parse_fetched(raw) -> date | None:
    if isinstance(raw, datetime):
        return raw.date()
    if isinstance(raw, date):
        return raw
    if isinstance(raw, str):
        try:
            return datetime.fromisoformat(raw.replace("Z", "+00:00")).date()
        except ValueError:
            return None
    return None


def build_snapshot_index() -> dict[str, date]:
    """Return a map of source_id -> latest fetched_at date across snapshots/.

    Walks the snapshots tree once instead of rescanning per source.
    """
    latest: dict[str, date] = {}
    if not SNAPSHOTS_ROOT.is_dir():
        return latest
    for meta in SNAPSHOTS_ROOT.rglob("*.meta.yaml"):
        try:
            with meta.open("r") as f:
                data = yaml.load(f)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        sid = data.get("source_id")
        d = _parse_fetched(data.get("fetched_at"))
        if not sid or d is None:
            continue
        if sid not in latest or d > latest[sid]:
            latest[sid] = d
    return latest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="fail on stale snapshots")
    args = parser.parse_args()

    if not REGISTRY.is_file():
        print(f"NOTE: registry not found: {REGISTRY}")
        print("Law-reference validation skipped (registry expected after framework-refs seeding).")
        return 0
    with REGISTRY.open("r") as f:
        data = yaml.load(f)
    sources = data.get("sources", []) if isinstance(data, dict) else []

    snapshot_index = build_snapshot_index()
    today = date.today()
    stale: list[str] = []
    for src in sources:
        sid = src.get("id")
        cadence = src.get("check_frequency_days", 90)
        if src.get("tracking_mode") == "metadata_only":
            continue
        last = snapshot_index.get(sid)
        if last is None:
            stale.append(f"{sid}: no snapshot found (cadence {cadence}d)")
            continue
        age = (today - last).days
        if age > cadence:
            stale.append(f"{sid}: snapshot age {age}d exceeds cadence {cadence}d")

    print(f"Checked {len(sources)} registered sources.")
    if stale:
        print(f"Stale sources ({len(stale)}):")
        for s in stale:
            print(f"  {s}")
        return 1 if args.strict else 0
    print("All source snapshots within cadence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
