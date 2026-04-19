---
doc_id: DOC-004
doc_type: standard
title: Standalone operation charter
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
  - iso27001:7.5.3
signature_ref: null
---

# Standalone operation charter

**DOC-004 Revision 1 (DRAFT)**

*Status: draft. Owner: role:ISMS-Manager. Next review: 2027-01-01.*

## 1. Principle

This repository operates without runtime dependency on external services, skill stacks, AI tooling, or platform-specific infrastructure. A fresh clone with Python 3.12+ and git must be able to run `make bootstrap`, `make validate`, and `make pack` end to end.

## 2. What standalone means

- Every validator in `tooling/validators/` runs against committed files only. No network calls.
- Every core collector in `tooling/collectors/core/` runs against committed files only. No network calls.
- Every packager in `tooling/packagers/` runs against committed files only. No network calls.
- The renderer (`tooling/instantiate.py`) runs against committed files only.
- `make validate`, `make currency-check`, `make pack`, and `make selbstdeklaration` all complete without network access.

## 3. What is explicitly optional

Network-dependent operations are confined to `tooling/collectors/optional/` and are invoked only via explicit targets:

- `make snapshot-fetch`: fetches law snapshots from RIS and EUR-Lex.
- Scheduled CI workflow `currency-check.yaml`: runs snapshot-fetch and delta detection weekly.
- Provider-specific collectors (Veeam, Keycloak, Wazuh, etc.): opt-in per instance, configured via `instance/config.yaml`.

Optional collectors failing due to network or credential issues must not break any required validation or packaging target.

## 4. What this repository must never depend on

- External AI services or skill stacks for runtime operation.
- Cloud-hosted GRC platforms (Drata, Vanta, Secureframe, ServiceNow GRC, OneTrust) for evidence storage or validation. Integration with such platforms is permitted via collectors but is not a dependency.
- Proprietary document management systems for governance artefacts. Markdown in git is the source of truth.
- External signing services as a validation dependency. QES signing via A-Trust or equivalent is used for legal signatures, but validator operation does not require QTSP availability.

## 5. Why

Audit evidence must be reproducible. A future auditor must be able to clone the repository, run the same tooling, and reach the same conclusions. An ISMS whose validation depends on a SaaS service that may go out of business, change pricing, or change APIs cannot guarantee this.

## 6. Verification

CI workflow `validate.yaml` runs on a fresh GitHub-hosted runner. If it passes there, standalone operation is verified.

## 7. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | 2026-04-19 | draft | initial draft |
