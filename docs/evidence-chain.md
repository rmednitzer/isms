---
doc_id: DOC-006
doc_type: standard
title: Evidence chain
revision: 1
status: draft
approved_date: null
approved_by: null
owner: role:ISMS-Manager
classification: internal
supersedes_revision: null
next_review: 2027-01-01
language: en
framework_refs:
  - iso27001:9.1
  - iso27001:9.2
  - iso27001:9.3
  - iso27001:10.1
signature_ref: null
---

# Evidence chain

**DOC-006 Revision 1 (DRAFT)**

*Status: draft. Owner: role:ISMS-Manager. Next review: 2027-01-01.*

## 1. Purpose

Specifies how evidence is collected, signed, stored, aged, and consumed for audit and supervisory purposes.

## 2. Three collection modes

### 2.1 API-pull

Used where the source system exposes a queryable API. A collector in `tooling/collectors/optional/` fetches structured data, normalises to the attestation schema, signs the attestation, commits to the evidence tree.

### 2.2 Agent-push

Used where the source system is isolated, API-restricted, or requires privileged local context. A small agent on the host collects on a schedule, produces a signed attestation, posts to a pickup endpoint; the orchestrator sweeps and commits.

### 2.3 Human-captured

Used where no API or agent is viable (legacy systems, vendor portals showing third-party data, physical observations). SOP-301 defines evidence tasks (ET-NNN). A guided capture produces a manual attestation that wraps the captured artefact (screenshot, export, photograph) with signed metadata.

## 3. Attestation schema

Per `tooling/schemas/attestation.schema.json`:

- schema_version
- control_id (must resolve in control catalogue)
- attestation_type
- collected_at (ISO 8601 with timezone)
- collected_by (person: or role: or collector path)
- source_system and source_system_instance
- collection_method (api_pull | agent_push | manual_screenshot | manual_export | manual_observation)
- period_covered (start and end)
- observations (structured payload specific to the control)
- raw_snapshot_hash (SHA-256 of the full source data if applicable)
- captured_files (list with path and sha256)
- signed_by
- signature_method (gpg | ssh | qes)

## 4. Storage layout

```
instance/evidence/
├── YYYY/
│   └── MM/
│       └── DD/
│           └── control-<ID>/
│               ├── <collector>-<timestamp>.json      attestation
│               ├── <collector>-<timestamp>.raw.json  source (where applicable)
│               ├── <collector>-<timestamp>.sig       detached signature
│               └── <collector>-<timestamp>.png       captured artefact (where applicable)
├── manifests/
│   ├── daily/YYYY-MM-DD.yaml.sig
│   ├── weekly/YYYY-WW.yaml.sig
│   └── monthly/YYYY-MM.yaml.sig
└── signatures/
    └── <doc_id>-R<rev>-<YYYY-MM-DD>.pdf      QES-signed governance PDFs
```

## 5. Manifests

A manifest is a signed YAML file enumerating evidence artefacts produced in a period with their hashes, forming a hash-chain. Daily manifests reference the previous day's manifest hash; weekly references the last daily; monthly references the last weekly. The chain is the audit-trail backbone.

## 6. Evidence plan

`template/governance/controls/evidence-plan.yaml` enumerates evidence tasks (ET-NNN), binding controls to cadences, owners, and collection methods. `tooling/collectors/core/evidence_age_report.py` reports aging.

## 7. Append-only

Evidence files are never modified. Corrections are additive: a new attestation supersedes, with `supersedes` field pointing to the earlier artefact. The earlier artefact remains.

## 8. Classification

Evidence defaults to confidential. See DOC-001 § 3 for classification options. Confidential evidence must not contain secrets (keys, passwords, customer PII excerpts); those are attested by metadata only, not captured.

## 9. Audit consumption

`make pack AUDIT=<stage>` assembles a curated bundle for an audit. Curation includes: all approved governance artefacts, recent evidence for in-scope controls, manifests, ceremony records, impact assessments, and decision records.

## 10. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | 2026-04-19 | draft | initial draft |
