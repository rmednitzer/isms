---
doc_id: DOC-003
doc_type: standard
title: Operating contract of the repository
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
  - iso27001:7.5
signature_ref: null
---

# Operating contract of the repository

**DOC-003 Revision 1 (DRAFT)**

*Status: draft. Owner: role:ISMS-Manager. Next review: 2027-01-01.*

## 1. Purpose

Describes how this repository operates end to end: layers, responsibilities, workflows, and constraints. Read before making any commit.

## 2. Layer model

Two layers plus shared infrastructure.

### 2.1 Template layer (`template/`)

Reusable framework. Entity-agnostic. Policies, procedures, and standards with `{{PLACEHOLDERS}}` that resolve against `instance/config.yaml`. Updating the template improves the framework for all future deployments and may produce pull-down changes for current instances.

### 2.2 Instance layer (`instance/`)

One concrete deployment. Entity-specific. Holds the rendered governance artefacts, operational state, evidence, and user-to-role bindings for a single organisation.

### 2.3 Shared infrastructure

- `docs/`: repo-level operating rules (this file, document control, signature policy, contribution flow, evidence chain, timeline, bilingualism).
- `framework-refs/`: authoritative law snapshots, registry, crosswalks, regulatory calendar. Universal content; which subset is activated is per-instance.
- `tooling/`: schemas, validators, collectors, signers, packagers, renderer.

## 3. Instantiation workflow

For a new deployment:

1. Fork or clone this repository.
2. Edit `instance/config.yaml` with entity details, role holders, provider bindings, feature flags.
3. Run `python tooling/instantiate.py --config instance/config.yaml`.
4. The renderer reads `template/`, resolves placeholders, and writes to `instance/`. Unresolved placeholders are a fatal error.
5. Commit the rendered instance alongside the config.
6. Re-run `instantiate` whenever `config.yaml` changes or the template is updated. Re-rendering is idempotent.

## 4. Change flow

Per `docs/contribution-flow.md`:

1. Open a branch from `main`.
2. Make changes (template edits, instance edits, tooling improvements, framework-ref updates).
3. Run `make validate` locally; must pass.
4. Open a PR; CI runs the validator suite plus signature verification.
5. CODEOWNER approval required per `.github/CODEOWNERS`.
6. PR merged with signed merge commit on `main`.

Governance artefacts transitioning to `status=approved` follow the QES signing flow per `docs/signature-policy.md` and SOP-201.

## 5. Evidence flow

Per `docs/evidence-chain.md`:

Three collection modes (API, agent, manual) writing to `instance/evidence/YYYY/MM/DD/control-<ID>/`. Each evidence artefact is a signed attestation plus the captured source. Daily, weekly, and monthly signed manifests hash-link the evidence tree. `make currency-check` reports aging and stale tasks.

## 6. Regulatory currency flow

Per SOP-101, SOP-102, SOP-103:

Sources listed in `framework-refs/sources/registry.yaml` are checked at their configured cadence. Deltas produce records under `framework-refs/currency/deltas/`. Material or structural changes trigger an impact assessment under `framework-refs/impact-assessments/`, which feeds artefact revisions and management review.

## 7. Incident flow

Per P-005, SOP-001, and the pre-filled Frühwarnung template:

Cybersecurity incidents meeting NISG 2026 significance thresholds are reported to CERT.at within 24 hours. The incident report is a direct operational action, not a pull request. Post-event, the incident record is created in `instance/operations/incidents/active/` and closed per SOP-001.

## 8. Audit flow

Per SOP-006 (internal audit), SOP-007 (management review), and the audit-pack packager:

Internal audits run per programme. External audits (stage 1, stage 2, surveillance, recertification) consume audit packs built via `make pack AUDIT=<stage>`. Findings become records in `instance/operations/audits/`; corrective actions feed the risk register and the continuous-improvement cycle.

## 9. Priority of concerns

When decisions conflict, priority order is: correctness over speed, safety over completeness, auditability over convenience, standalone over integrated.

## 10. Out of scope

This document does not describe how to implement controls. That is the content of policies, SOPs, and standards under `governance/`. It does not prescribe technology choices; those are per-instance in `instance/config.yaml`.

## 11. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | 2026-04-19 | draft | initial draft |
