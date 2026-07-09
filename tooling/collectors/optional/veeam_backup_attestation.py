#!/usr/bin/env python3
"""
Backup-attestation evidence collector (backup provider, e.g. Veeam).

Evidence for A.8.13 Information backup: pulls recent backup/restore-test job
state from the configured backup provider. Config: providers.backup in
instance/config.yaml. Offline/unconfigured runs emit a not_collected attestation.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _provider_common import run_collector


def main() -> int:
    return run_collector(
        category="backup",
        control_id="A.8.13",
        attestation_type="backup_attestation",
        source_system_default="backup-provider",
        collector_path="tooling/collectors/optional/veeam_backup_attestation.py",
    )


if __name__ == "__main__":
    sys.exit(main())
