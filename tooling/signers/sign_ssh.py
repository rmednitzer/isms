#!/usr/bin/env python3
"""
SSH signing wrapper. Produces detached SSH signatures per RFC 4253 via ssh-keygen -Y sign.

Usage: python sign_ssh.py <path> --key KEYFILE --namespace git

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
    parser.add_argument("--key", required=True, help="SSH private key file")
    parser.add_argument("--namespace", default="file", help="signature namespace")
    args = parser.parse_args()

    if not args.path.is_file():
        print(f"ERROR: not a file: {args.path}", file=sys.stderr)
        return 2

    cmd = ["ssh-keygen", "-Y", "sign", "-f", args.key, "-n", args.namespace, str(args.path)]
    try:
        subprocess.check_call(cmd)
    except FileNotFoundError:
        print("ERROR: ssh-keygen not installed", file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as e:
        print(f"ERROR: ssh-keygen failed: {e}", file=sys.stderr)
        return 1
    print(f"Signed: {args.path}.sig")
    return 0


if __name__ == "__main__":
    sys.exit(main())
