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

import sys

from _common import GOVERNANCE_SCAN_ROOTS, REPO_ROOT, iter_frontmatter

SIGNED_DOC_TYPES = {"policy", "plan"}


def main() -> int:
    violations: list[str] = []
    checked = 0
    for md, fm in iter_frontmatter(GOVERNANCE_SCAN_ROOTS):
        if fm.get("status") != "approved":
            continue
        if fm.get("doc_type") not in SIGNED_DOC_TYPES:
            continue
        checked += 1
        sig_ref = fm.get("signature_ref")
        interim = fm.get("interim_signature", False)
        if not sig_ref and not interim:
            violations.append(
                f"{md}: approved policy/plan without signature_ref and without interim_signature=true"
            )
        elif sig_ref and not (REPO_ROOT / sig_ref).exists():
            violations.append(f"{md}: signature_ref path does not exist: {sig_ref}")

    print(f"Checked signature references across {checked} approved policy/plan artefacts.")
    if violations:
        print(f"{len(violations)} violations:")
        for v in violations:
            print(f"  {v}")
        return 1
    print("Signature references consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
