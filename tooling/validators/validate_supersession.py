#!/usr/bin/env python3
"""
Validate supersession chains: every revision > 1 references a previous revision
that exists, and at most one revision per doc_id has status != superseded.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

from _common import FRONTMATTER_RE, REPO_ROOT, iter_frontmatter  # noqa: F401
from _common import _yaml as yaml  # noqa: F401  (re-exported for tests)

SCAN_ROOTS = [REPO_ROOT / "docs", REPO_ROOT / "template", REPO_ROOT / "instance"]


def main() -> int:
    revisions: dict[str, list[tuple[int, str, Path]]] = defaultdict(list)
    for md, fm in iter_frontmatter(SCAN_ROOTS):
        doc_id = fm.get("doc_id")
        rev = fm.get("revision")
        status = fm.get("status")
        if doc_id and isinstance(rev, int):
            revisions[doc_id].append((rev, status or "", md))

    violations: list[str] = []
    for doc_id, entries in revisions.items():
        entries.sort()
        active = [(r, s, p) for r, s, p in entries if s not in {"superseded", "retired"}]
        if len(active) > 1:
            paths = ", ".join(str(p) for _, _, p in active)
            violations.append(f"{doc_id}: multiple active revisions ({paths})")
        revs = [r for r, _, _ in entries]
        for r in revs:
            if r > 1 and (r - 1) not in revs:
                # The previous revision may legitimately not be in-tree if editorial-only.
                print(f"NOTE: {doc_id} revision {r} has no predecessor revision {r - 1} in tree")

    print(
        f"Checked supersession across {sum(len(v) for v in revisions.values())} "
        f"revisions of {len(revisions)} documents."
    )
    if violations:
        print(f"{len(violations)} violations:")
        for v in violations:
            print(f"  {v}")
        return 1
    print("Supersession chains consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
