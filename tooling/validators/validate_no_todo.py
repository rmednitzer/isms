#!/usr/bin/env python3
"""
Reject placeholder residue in rendered instance artefacts.

The template layer legitimately contains ``TODO:`` markers and ``{{placeholder}}``
tokens; the instance layer, once rendered from config, must not. instantiate.py
only detects a *missing* config key, so a config value like
"TODO: Example Organisation GmbH" renders verbatim and slips through. This
validator scans committed instance governance/operations artefacts and fails on
any residual ``TODO:`` sentinel or unresolved ``{{...}}`` placeholder.

Exits 0 on success, 1 on violations, 2 on infrastructure errors.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _common import REPO_ROOT

SCAN_ROOTS = (
    REPO_ROOT / "instance" / "governance",
    REPO_ROOT / "instance" / "operations",
    REPO_ROOT / "instance" / "users",
)
SCAN_SUFFIXES = {".md", ".yaml", ".yml"}
TODO_RE = re.compile(r"\bTODO:", re.IGNORECASE)
PLACEHOLDER_RE = re.compile(r"\{\{.*?\}\}")


def scan_file(path: Path) -> list[str]:
    problems: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for n, line in enumerate(text.splitlines(), start=1):
        if TODO_RE.search(line):
            problems.append(f"{path}:{n}: residual TODO sentinel")
        if PLACEHOLDER_RE.search(line):
            problems.append(f"{path}:{n}: unresolved placeholder token")
    return problems


def main() -> int:
    violations: list[str] = []
    scanned = 0
    for root in SCAN_ROOTS:
        if not root.is_dir():
            continue
        for f in root.rglob("*"):
            if f.is_file() and f.suffix in SCAN_SUFFIXES and f.name != ".gitkeep":
                scanned += 1
                violations.extend(scan_file(f))

    print(f"Scanned {scanned} rendered instance artefacts for placeholder residue.")
    if violations:
        print(f"{len(violations)} violations:")
        for v in violations:
            print(f"  {v}")
        print("Populate instance/config.yaml (replace TODO: values) and re-run make instantiate.")
        return 1
    print("No residual TODO: sentinels or unresolved placeholders in instance artefacts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
