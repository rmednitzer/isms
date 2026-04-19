#!/usr/bin/env bash
# Human-captured evidence wrapper.
# Guides an operator through capturing manual evidence for an evidence task,
# stages the attestation YAML, and commits.
#
# Usage: ./tooling/capture.sh <ET-NNN>
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
DATE="$(date -u +%Y-%m-%d)"
YEAR="$(date -u +%Y)"
MONTH="$(date -u +%m)"
DAY="$(date -u +%d)"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

echo "Evidence capture for ${ET}"
read -r -p "Control ID (e.g. A.8.13): " CONTROL_ID
read -r -p "Source system (e.g. Veeam B&R v12): " SOURCE_SYSTEM
read -r -p "Source system instance (hostname/url): " SOURCE_INSTANCE
read -r -p "Capture method [manual_screenshot|manual_export|manual_observation]: " METHOD
METHOD="${METHOD:-manual_screenshot}"
echo "Reviewer notes (end with Ctrl-D):"
NOTES="$(cat)"

OUT_DIR="${REPO_ROOT}/instance/evidence/${YEAR}/${MONTH}/${DAY}/control-${CONTROL_ID}"
mkdir -p "${OUT_DIR}"

ATT_PATH="${OUT_DIR}/${ET}-${STAMP}.yaml"
cat > "${ATT_PATH}" <<EOF
schema_version: 1
control_id: ${CONTROL_ID}
attestation_type: manual_review
evidence_task_id: ${ET}
collected_at: $(date -u +%Y-%m-%dT%H:%M:%SZ)
collected_by: person:$(git config user.name | tr -d ' ' | tr '[:upper:]' '[:lower:]' || echo unknown)
collection_method: ${METHOD}
source_system: "${SOURCE_SYSTEM}"
source_system_instance: "${SOURCE_INSTANCE}"
captured_files: []
reviewer_notes: |
$(echo "${NOTES}" | sed 's/^/  /')
EOF

if [[ $# -gt 0 ]]; then
    for f in "$@"; do
        if [[ -f "$f" ]]; then
            base="$(basename "$f")"
            cp "$f" "${OUT_DIR}/${base}"
            sha="$(sha256sum "${OUT_DIR}/${base}" | awk '{print $1}')"
            python3 -c "
import sys
from ruamel.yaml import YAML
y = YAML(typ='rt')
with open('${ATT_PATH}') as fp:
    d = y.load(fp)
d['captured_files'].append({'path': '${base}', 'sha256': '${sha}'})
with open('${ATT_PATH}', 'w') as fp:
    y.dump(d, fp)
"
        fi
    done
fi

echo ""
echo "Attestation staged: ${ATT_PATH}"
echo "Review, then sign with: python tooling/signers/sign_gpg.py ${ATT_PATH}"
echo "Then commit."
