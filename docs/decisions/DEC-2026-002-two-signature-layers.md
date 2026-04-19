---
doc_id: DEC-2026-002
doc_type: record
title: "Two signature layers"
revision: 1
status: approved
approved_date: 2026-04-19
approved_by: role:CISO
owner: role:CISO
classification: internal
supersedes_revision: null
next_review: 2028-04-19
language: en
framework_refs:
  - iso27001:7.5.3
signature_ref: null
interim_signature: true
---

# Two signature layers

**DEC-2026-002 Revision 1 - 2026-04-19**

*Status: approved. Owner: role:CISO. Next review: 2028-04-19.*

*Interim: legal signature pending QES integration. Approved via git-level only.*

## Context

Git commit signatures are not eIDAS signatures. Equating them is a legal category error that auditors increasingly catch. ISO 27001 clause 7.5.3 and NISG 2026 § 31 call for evidenced approval at appropriate management level, which QES establishes with non-repudiation. Git-sig is necessary for internal integrity but insufficient for legal weight.

## Decision

Governance artefacts carry two distinct signatures: git-level (GPG or SSH-sig on commits) for integrity and authorship, and eIDAS QES (PAdES-signed PDF) for legal approval of policies, plans, SoA, management review minutes, audit statements, and Selbstdeklaration.

## Alternatives considered

Alternative 1: git-sig only. Rejected because it does not satisfy eIDAS Art. 25(2) handwritten-equivalent effect that regulators expect for Leitungsorgan approvals.
Alternative 2: QES on every commit. Rejected because it is operationally infeasible at commit cadence and wastes QTSP transactions on non-governance changes.

## Consequences

Implementation cost: QTSP contract, signing pipeline, SOP-201 ceremony, 90-day interim posture acceptable during onboarding.

## Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | 2026-04-19 | approved | initial record |
