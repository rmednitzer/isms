#!/usr/bin/env python3
"""
Validate signature references and signed-commit policy hints.

- For every artefact with status=approved and signature_ref set, structurally
  verify the reference (Hard Rule 3: no fabricated signature_ref): the path
  must be repo-relative, resolve inside instance/evidence/signatures/, and
  point at a regular, non-empty file whose first bytes are the %PDF magic.
- This is a structural check, not cryptographic verification. PAdES/QES
  signature validity is verified separately at commit time via git signing
  configuration and by tooling/signers/verify_qes.py for QES artefacts.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from _common import GOVERNANCE_SCAN_ROOTS, REPO_ROOT, iter_frontmatter

SIGNED_DOC_TYPES = {"policy", "plan"}
SIGNATURES_DIR = (REPO_ROOT / "instance" / "evidence" / "signatures").resolve()
PDF_MAGIC = b"%PDF"
# Markers of an embedded PDF signature (PAdES / PKCS#7). A rendered but unsigned
# PDF, or a hand-crafted file with only a %PDF header, contains none of these.
# This is a structural presence check, not cryptographic validation: full QES
# verification (cert chain, PAdES level, revocation) is still deferred to an
# EU DSS binding in verify_qes.py once implemented.
PDF_SIG_SUBFILTERS = (
    b"/ETSI.CAdES.detached",
    b"/ETSI.RFC3161",
    b"/adbe.pkcs7.detached",
    b"/adbe.pkcs7.sha1",
    b"/adbe.x509.rsa_sha1",
)
INTERIM_SIGNATURE_WINDOW_DAYS = 90


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
        blob = target.read_bytes()
    except OSError as exc:
        return f"signature_ref unreadable ({exc}): {sig_ref}"
    if not blob:
        return f"signature_ref file is empty: {sig_ref}"
    if not blob.startswith(PDF_MAGIC):
        return f"signature_ref is not a PDF (missing %PDF header): {sig_ref}"
    if b"/ByteRange" not in blob or not any(sf in blob for sf in PDF_SIG_SUBFILTERS):
        return (
            "signature_ref PDF contains no embedded PAdES/PKCS7 signature "
            f"(/ByteRange + signature /SubFilter absent): {sig_ref}"
        )
    return None


def check_interim_window(fm: dict) -> str | None:
    """Return a problem if an interim-signed approval has outlived the window.

    DOC-002 section 5: interim posture is time-bounded. An approval carrying
    interim_signature=true whose approved_date is more than 90 days ago is an
    audit finding and must obtain a real QES.
    """
    approved = fm.get("approved_date")
    if not approved:
        return "interim_signature=true but no approved_date to bound the 90-day window"
    try:
        approved_date = date.fromisoformat(str(approved))
    except ValueError:
        return f"interim_signature approved_date not an ISO date: {approved!r}"
    age = (date.today() - approved_date).days
    if age > INTERIM_SIGNATURE_WINDOW_DAYS:
        return (
            f"interim_signature has lapsed: approved {age}d ago exceeds the "
            f"{INTERIM_SIGNATURE_WINDOW_DAYS}-day window (DOC-002 section 5); obtain a QES"
        )
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
        elif interim and not sig_ref:
            problem = check_interim_window(fm)
            if problem:
                violations.append(f"{md}: {problem}")
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
