#!/usr/bin/env python3
"""
Validate bilingual parity where declared.

An artefact with front-matter bilingual=true must have both <name>.en.md and
<name>.de.md (or equivalent) present in the same directory.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
yaml = YAML(typ="safe")


def main() -> int:
    violations: list[str] = []
    checked = 0
    for md in REPO_ROOT.rglob("*.md"):
        if "/.venv/" in str(md) or "/__pycache__/" in str(md):
            continue
        text = md.read_text(encoding="utf-8")
        m = FRONTMATTER_RE.match(text)
        if not m:
            continue
        fm = yaml.load(m.group(1)) or {}
        if not isinstance(fm, dict):
            continue
        if not fm.get("bilingual"):
            continue
        checked += 1
        # Expect companion file with alternate language suffix
        name = md.stem
        lang = fm.get("language", "en")
        other_lang = "de" if lang == "en" else "en"
        # Strip trailing .xx if present, else use bare name
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
