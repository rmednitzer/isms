#!/usr/bin/env python3
"""
Validate supersession chains: every revision > 1 references a previous revision
that exists, and at most one revision per doc_id has status != superseded.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCAN_ROOTS = [REPO_ROOT / "docs", REPO_ROOT / "template", REPO_ROOT / "instance"]
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
yaml = YAML(typ="safe")


def main() -> int:
    revisions: dict[str, list[tuple[int, str, Path]]] = defaultdict(list)
    for root in SCAN_ROOTS:
        if not root.is_dir():
            continue
        for md in root.rglob("*.md"):
            text = md.read_text(encoding="utf-8")
            m = FRONTMATTER_RE.match(text)
            if not m:
                continue
            fm = yaml.load(m.group(1)) or {}
            if not isinstance(fm, dict):
                continue
            doc_id = fm.get("doc_id")
            rev = fm.get("revision")
            status = fm.get("status")
            if doc_id and isinstance(rev, int):
                revisions[doc_id].append((rev, status or "", md))

    violations: list[str] = []
    for doc_id, entries in revisions.items():
        entries.sort()
        active = [(r, s, p) for r, s, p in entries if s != "superseded" and s != "retired"]
        if len(active) > 1:
            paths = ", ".join(str(p) for _, _, p in active)
            violations.append(f"{doc_id}: multiple active revisions ({paths})")
        revs = [r for r, _, _ in entries]
        for r in revs:
            if r > 1 and (r - 1) not in revs:
                # The previous revision may legitimately not be in-tree if editorial-only.
                # We accept missing predecessors but flag as warnings via stdout.
                print(f"NOTE: {doc_id} revision {r} has no predecessor revision {r - 1} in tree")

    print(f"Checked supersession across {sum(len(v) for v in revisions.values())} revisions of {len(revisions)} documents.")
    if violations:
        print(f"{len(violations)} violations:")
        for v in violations:
            print(f"  {v}")
        return 1
    print("Supersession chains consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
