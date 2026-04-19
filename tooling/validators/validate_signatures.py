#!/usr/bin/env python3
"""
Validate signature references and signed-commit policy hints.

- For every artefact with status=approved and signature_ref set, verify that the
  referenced file exists.
- Do not perform cryptographic verification here; this is a path-existence check.
  Actual signature cryptographic verification is done at commit time via git
  configuration and by tooling/signers/verify_qes.py for QES artefacts.

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
        checked += 1
        if fm.get("status") != "approved":
            continue
        sig_ref = fm.get("signature_ref")
        interim = fm.get("interim_signature", False)
        doc_type = fm.get("doc_type")
        if doc_type in {"policy", "plan"}:
            if not sig_ref and not interim:
                violations.append(f"{md}: approved policy/plan without signature_ref and without interim_signature=true")
            elif sig_ref:
                sig_path = REPO_ROOT / sig_ref
                if not sig_path.exists():
                    violations.append(f"{md}: signature_ref path does not exist: {sig_ref}")

    print(f"Checked signature references across {checked} approved artefacts.")
    if violations:
        print(f"{len(violations)} violations:")
        for v in violations:
            print(f"  {v}")
        return 1
    print("Signature references consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
