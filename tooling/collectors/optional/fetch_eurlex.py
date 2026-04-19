#!/usr/bin/env python3
"""
Fetch EU law snapshots from EUR-Lex by CELEX identifier.

Documentation: https://eur-lex.europa.eu

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
REGISTRY = REPO_ROOT / "framework-refs" / "sources" / "registry.yaml"
yaml = YAML(typ="rt")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-id")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not REGISTRY.is_file():
        print(f"NOTE: registry not found: {REGISTRY}")
        return 0
    with REGISTRY.open("r") as f:
        data = yaml.load(f)
    sources = data.get("sources", []) if isinstance(data, dict) else []
    eu_sources = [s for s in sources if s.get("fetch_method") == "eurlex_api"]
    if args.source_id:
        eu_sources = [s for s in eu_sources if s.get("id") == args.source_id]

    print(f"Would fetch {len(eu_sources)} EUR-Lex sources:")
    for s in eu_sources:
        print(f"  {s.get('id')}: CELEX {s.get('celex')}, {s.get('authoritative_url')}")

    # TODO: implement EUR-Lex REST API fetching. Options:
    # - SPARQL endpoint: https://publications.europa.eu/webapi/rdf/sparql
    # - Cellar: https://publications.europa.eu/resource/celex/<CELEX>
    # - HTML fetch with language preference header (de-AT, en)
    # For each source, fetch latest consolidated version by CELEX; write XML and
    # normalised markdown to framework-refs/snapshots/eu/<source>/ with meta yaml.
    print()
    print("NOTE: EUR-Lex binding not yet implemented. Skeleton ready for extension.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
