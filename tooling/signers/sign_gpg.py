#!/usr/bin/env python3
"""
GPG signing wrapper. Produces detached signatures.

Usage: python sign_gpg.py <path> [--key KEYID]

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--key", help="GPG key ID or fingerprint")
    args = parser.parse_args()

    if not args.path.is_file():
        print(f"ERROR: not a file: {args.path}", file=sys.stderr)
        return 2

    cmd = ["gpg", "--detach-sign", "--armor"]
    if args.key:
        cmd.extend(["--local-user", args.key])
    cmd.extend(["--output", str(args.path) + ".sig", str(args.path)])

    try:
        subprocess.check_call(cmd)
    except FileNotFoundError:
        print("ERROR: gpg not installed", file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as e:
        print(f"ERROR: gpg failed: {e}", file=sys.stderr)
        return 1
    print(f"Signed: {args.path}.sig")
    return 0


if __name__ == "__main__":
    sys.exit(main())
