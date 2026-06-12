#!/usr/bin/env bash
# Human-captured evidence wrapper.
# Guides an operator through capturing manual evidence for an evidence task,
# stages the attestation YAML, and prints next steps (review, sign, commit).
#
# Usage: bash tooling/capture.sh <ET-NNN> [optional attachment paths...]
#
# Security note: every operator-supplied value (interactive fields, reviewer
# notes, and attachment filenames) is passed to the Python helper through the
# environment and argv. Nothing is interpolated into shell command text or into
# Python source. The heredoc delimiter is quoted so the Python body is literal.
# This is deliberate: filenames and pasted notes are untrusted input.
#
# Copyright 2026 isms contributors
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <ET-NNN> [optional attachment paths...]"
    exit 2
fi

ET="$1"
shift
REPO_ROOT="$(git rev-parse --show-toplevel)"
YEAR="$(date -u +%Y)"
MONTH="$(date -u +%m)"
DAY="$(date -u +%d)"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
COLLECTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "Evidence capture for ${ET}"
read -r -p "Control ID (e.g. A.8.13): " CONTROL_ID
read -r -p "Source system (e.g. Veeam B&R v12): " SOURCE_SYSTEM
read -r -p "Source system instance (hostname/url): " SOURCE_INSTANCE
read -r -p "Capture method [manual_screenshot|manual_export|manual_observation]: " METHOD
METHOD="${METHOD:-manual_screenshot}"
echo "Reviewer notes (end with Ctrl-D):"
NOTES="$(cat)"

# Control IDs are short identifiers. Reject anything that could traverse the
# evidence tree or inject a path separator before it is used to build OUT_DIR.
if [[ ! "${CONTROL_ID}" =~ ^[A-Za-z0-9._-]+$ ]]; then
    echo "ERROR: invalid control id '${CONTROL_ID}'; expected pattern [A-Za-z0-9._-]+" >&2
    exit 2
fi

OUT_DIR="${REPO_ROOT}/instance/evidence/${YEAR}/${MONTH}/${DAY}/control-${CONTROL_ID}"
mkdir -p "${OUT_DIR}"
ATT_PATH="${OUT_DIR}/${ET}-${STAMP}.yaml"

COLLECTED_BY="person:$(git config user.name 2>/dev/null | tr -d ' ' | tr '[:upper:]' '[:lower:]' || true)"
COLLECTED_BY="${COLLECTED_BY:-person:unknown}"

ET="${ET}" \
CONTROL_ID="${CONTROL_ID}" \
ATTESTATION_TYPE="manual_review" \
COLLECTED_AT="${COLLECTED_AT}" \
COLLECTED_BY="${COLLECTED_BY}" \
METHOD="${METHOD}" \
SOURCE_SYSTEM="${SOURCE_SYSTEM}" \
SOURCE_INSTANCE="${SOURCE_INSTANCE}" \
NOTES="${NOTES}" \
ATT_PATH="${ATT_PATH}" \
OUT_DIR="${OUT_DIR}" \
python3 - "$@" <<'PY'
import hashlib
import os
import shutil
import sys
from pathlib import Path

from ruamel.yaml import YAML

out_dir = Path(os.environ["OUT_DIR"])
att_path = Path(os.environ["ATT_PATH"])

captured = []
for src in sys.argv[1:]:
    p = Path(src)
    if not p.is_file():
        print(f"WARNING: attachment not found, skipping: {src}", file=sys.stderr)
        continue
    dest = out_dir / p.name
    shutil.copy2(p, dest)
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    captured.append({"path": p.name, "sha256": digest})

doc = {
    "schema_version": 1,
    "control_id": os.environ["CONTROL_ID"],
    "attestation_type": os.environ["ATTESTATION_TYPE"],
    "evidence_task_id": os.environ["ET"],
    "collected_at": os.environ["COLLECTED_AT"],
    "collected_by": os.environ["COLLECTED_BY"],
    "collection_method": os.environ["METHOD"],
    "source_system": os.environ["SOURCE_SYSTEM"],
    "source_system_instance": os.environ["SOURCE_INSTANCE"],
    "captured_files": captured,
    "reviewer_notes": os.environ["NOTES"],
}

yaml = YAML(typ="rt")
yaml.default_flow_style = False
with att_path.open("w", encoding="utf-8") as fh:
    yaml.dump(doc, fh)
PY

echo ""
echo "Attestation staged: ${ATT_PATH}"
echo "Review, then sign with: python tooling/signers/sign_gpg.py ${ATT_PATH}"
echo "Then commit."
