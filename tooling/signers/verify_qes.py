#!/usr/bin/env python3
"""
QES verification stub. Production implementation uses EU DSS (Digital Signature
Service by European Commission, https://github.com/esig/dss) or the QTSP's
verification endpoint.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path, help="signed PDF to verify")
    args = parser.parse_args()

    if not args.pdf.is_file():
        print(f"ERROR: not a file: {args.pdf}", file=sys.stderr)
        return 2

    print(f"Verifying QES on {args.pdf}")
    print("Stub. Implement via EU DSS library or QTSP verification endpoint.")
    print("Expected fields: signer certificate chain, qualified status,")
    print("PAdES level (B-B, B-T, B-LT, B-LTA), signing timestamp, revocation check.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
