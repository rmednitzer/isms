#!/usr/bin/env python3
"""
Validate bilingual parity where declared.

An artefact with front-matter bilingual=true must have both <name>.en.md and
<name>.de.md (or equivalent) present in the same directory.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import sys

from _common import (
    FRONTMATTER_RE,  # noqa: F401  (re-exported for tests)
    GOVERNANCE_SCAN_ROOTS,
    iter_frontmatter,
)
from _common import (
    _yaml as yaml,  # noqa: F401  (re-exported for tests)
)


def main() -> int:
    violations: list[str] = []
    checked = 0
    for md, fm in iter_frontmatter(GOVERNANCE_SCAN_ROOTS):
        if not fm.get("bilingual"):
            continue
        checked += 1
        name = md.stem
        lang = fm.get("language", "en")
        other_lang = "de" if lang == "en" else "en"
        if name.endswith(f".{lang}"):
            base = name[: -(len(lang) + 1)]
            companion = md.parent / f"{base}.{other_lang}.md"
        else:
            companion = md.parent / f"{name}.{other_lang}.md"
        if not companion.is_file():
            violations.append(f"{md}: declared bilingual but companion {companion.name} not found")

    print(f"Checked bilingual parity on {checked} declared-bilingual artefacts.")
    if violations:
        for v in violations:
            print(f"  {v}")
        return 1
    print("Bilingual parity OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
