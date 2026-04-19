#!/usr/bin/env python3
"""
Fetch law snapshots from the Austrian RIS (Rechtsinformationssystem des Bundes)
OpenData API. Stub implementation with defensive structure; full RIS API binding
depends on which laws are in scope per framework-refs/sources/registry.yaml.

Documentation: https://www.data.gv.at (search "RIS") and https://www.ris.bka.gv.at

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
REGISTRY = REPO_ROOT / "framework-refs" / "sources" / "registry.yaml"
SNAPSHOTS = REPO_ROOT / "framework-refs" / "snapshots"
yaml = YAML(typ="rt")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-id", help="fetch specific source only (default: all with fetch_method=ris_api)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        import requests  # noqa: F401
    except ImportError:
        print("requests library required; install with: pip install -e tooling/[dev]", file=sys.stderr)
        return 2

    if not REGISTRY.is_file():
        print(f"NOTE: registry not found: {REGISTRY}")
        return 0
    with REGISTRY.open("r") as f:
        data = yaml.load(f)
    sources = data.get("sources", []) if isinstance(data, dict) else []
    ris_sources = [s for s in sources if s.get("fetch_method") == "ris_api"]
    if args.source_id:
        ris_sources = [s for s in ris_sources if s.get("id") == args.source_id]

    if not ris_sources:
        print("No RIS-API sources configured; nothing to fetch.")
        return 0

    print(f"Would fetch {len(ris_sources)} RIS sources:")
    for s in ris_sources:
        print(f"  {s.get('id')}: {s.get('authoritative_url')}")

    if args.dry_run:
        return 0

    # TODO: implement actual RIS API fetching per
    # https://data.bka.gv.at/ris/api/v2.6 endpoints. For each source:
    # 1. Fetch consolidated text (by Gesetzesnummer or BGBl reference).
    # 2. Write raw XML + normalised markdown to framework-refs/snapshots/<jurisdiction>/<source>/.
    # 3. Write .meta.yaml with version_identifier, version_date, hashes, signed_at.
    # 4. Invoke signers/sign_gpg.py on the meta file.
    #
    # Defensive parsing: RIS API paginates at 100 entries, some metadata is in
    # inconsistent shapes between endpoints. Prefer the /Bundesrecht/Abfrage
    # and /Bundesgesetzblatt endpoints.
    print()
    print("NOTE: RIS API binding not yet implemented. Skeleton ready for extension.")
    print("      See docstring and registry.yaml per-source configuration.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
