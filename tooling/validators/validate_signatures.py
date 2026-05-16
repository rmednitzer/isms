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
from pathlib import Path

from _common import GOVERNANCE_SCAN_ROOTS, REPO_ROOT, iter_frontmatter

SIGNED_DOC_TYPES = {"policy", "plan"}
SIGNATURES_DIR = (REPO_ROOT / "instance" / "evidence" / "signatures").resolve()
PDF_MAGIC = b"%PDF"


def check_signature_ref(sig_ref: str) -> str | None:
    """Return a human-readable problem with ``sig_ref``, or None if it is sound.

    Existence alone is not enough (Hard Rule 3: no fabricated signature_ref).
    The target must be a regular, non-empty PDF inside the append-only
    signatures directory.
    """
    if Path(sig_ref).is_absolute():
        return f"signature_ref must be repo-relative, got absolute path: {sig_ref}"
    target = (REPO_ROOT / sig_ref).resolve()
    if not target.is_relative_to(SIGNATURES_DIR):
        return f"signature_ref escapes instance/evidence/signatures/: {sig_ref}"
    if not target.is_file():
        return f"signature_ref path does not exist or is not a regular file: {sig_ref}"
    try:
        header = target.read_bytes()[:5]
    except OSError as exc:
        return f"signature_ref unreadable ({exc}): {sig_ref}"
    if not header:
        return f"signature_ref file is empty: {sig_ref}"
    if not header.startswith(PDF_MAGIC):
        return f"signature_ref is not a PDF (missing %PDF header): {sig_ref}"
    return None


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
        elif sig_ref:
            problem = check_signature_ref(str(sig_ref))
            if problem:
                violations.append(f"{md}: {problem}")

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
