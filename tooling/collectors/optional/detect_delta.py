#!/usr/bin/env python3
"""
Detect deltas between the latest snapshot and the prior snapshot per source.

A delta is classified as editorial, minor, material, structural, or
new_subordinate_instrument. First-pass classification is automated based on
text-diff heuristics; human confirmation is required for any non-editorial
classification via SOP-102.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SNAPSHOTS = REPO_ROOT / "framework-refs" / "snapshots"
DELTAS = REPO_ROOT / "framework-refs" / "currency" / "deltas"


def main() -> int:
    if not SNAPSHOTS.is_dir():
        print("NOTE: no snapshots yet; nothing to compare.")
        return 0
    print("Delta detection skeleton; actual implementation compares newest .meta.yaml")
    print("pairs per source and emits DLT-YYYY-NNN records when hashes diverge.")
    print("Classification heuristic: structural > 20% text change, material > 5%,")
    print("minor > 0.1%, editorial otherwise. Human confirmation via SOP-102.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
