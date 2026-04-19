#!/usr/bin/env python3
"""
A-Trust Signatur-Box QES client stub.

This is a stub for the A-Trust PAdES signing integration. Implementing requires
an active A-Trust business contract and credentials. The real client wraps the
A-Trust Signatur-Box REST API to apply a qualified electronic signature in PAdES
format to a PDF and returns the signed PDF plus the transaction reference.

Documentation: https://www.a-trust.at

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path, help="input PDF to sign")
    parser.add_argument("--signer-role", required=True, help="role holder ID (e.g. person:alice)")
    parser.add_argument("--output", type=Path, help="output signed PDF path")
    args = parser.parse_args()

    print("A-Trust QES client stub.")
    print(f"Would sign: {args.pdf}")
    print(f"Signer: {args.signer_role}")
    print(f"Output: {args.output or str(args.pdf).replace('.pdf', '.signed.pdf')}")
    print()
    print("To implement:")
    print("  1. Acquire A-Trust business contract and signing credentials.")
    print("  2. Bind credentials via instance/config.yaml providers.qts_provider and external secret manager.")
    print("  3. Wrap Signatur-Box API calls (PKCS#11 or REST per contract).")
    print("  4. Return signed PDF plus transaction reference for the ceremony record.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
