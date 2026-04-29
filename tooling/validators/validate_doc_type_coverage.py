#!/usr/bin/env python3
"""
Validate style-guide coverage across document types.

Every `doc_type` enum value declared in
`tooling/schemas/frontmatter.schema.json` must have at least one artefact
present under `template/` whose front-matter uses it. This guarantees that
downstream deployments have a starting skeleton for every document kind
the schema permits and that DOC-009 section 7 (section skeleton by
document type) has a corresponding template.

Exits 0 on success, 1 on missing coverage, 2 on infrastructure errors.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from _common import REPO_ROOT, iter_markdown, parse_frontmatter

SCHEMA_PATH = REPO_ROOT / "tooling" / "schemas" / "frontmatter.schema.json"
TEMPLATE_ROOT = REPO_ROOT / "template"


def load_allowed_doc_types() -> list[str]:
    if not SCHEMA_PATH.is_file():
        print(f"ERROR: schema not found: {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(2)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        return list(schema["properties"]["doc_type"]["enum"])
    except KeyError:
        print("ERROR: schema missing doc_type enum", file=sys.stderr)
        sys.exit(2)


def collect_template_doc_types() -> dict[str, list[Path]]:
    found: dict[str, list[Path]] = {}
    for md_path in iter_markdown([TEMPLATE_ROOT]):
        fm = parse_frontmatter(md_path)
        if fm is None:
            continue
        doc_type = fm.get("doc_type")
        if not isinstance(doc_type, str):
            continue
        found.setdefault(doc_type, []).append(md_path.relative_to(REPO_ROOT))
    return found


def main() -> int:
    allowed = load_allowed_doc_types()
    found = collect_template_doc_types()

    missing = [dt for dt in allowed if dt not in found]
    extra = [dt for dt in found if dt not in allowed]

    for dt in allowed:
        examples = found.get(dt, [])
        first = examples[0] if examples else "MISSING"
        print(f"  {dt:10s}  {len(examples):4d}  {first}")

    if extra:
        print("\nTemplates declare doc_type values not in the schema:", file=sys.stderr)
        for dt in extra:
            print(f"  {dt}: {found[dt][0]}", file=sys.stderr)

    if missing:
        print(
            "\nFAIL: no template found for doc_type(s): " + ", ".join(missing),
            file=sys.stderr,
        )
        print(
            "Add a template under template/ that declares the missing "
            "doc_type, or remove the value from the schema.",
            file=sys.stderr,
        )
        return 1

    if extra:
        return 1

    print("\nOK: every schema doc_type has at least one template.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
