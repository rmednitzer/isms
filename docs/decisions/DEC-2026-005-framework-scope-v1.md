---
doc_id: DEC-2026-005
doc_type: record
title: "Framework scope v1"
revision: 1
status: approved
approved_date: 2026-04-19
approved_by: role:ISMS-Manager
owner: role:ISMS-Manager
classification: internal
supersedes_revision: null
next_review: 2028-04-19
language: en
framework_refs:
  - iso27001:7.5.3
signature_ref: null
interim_signature: true
---

# Framework scope v1

**DEC-2026-005 Revision 1 - 2026-04-19**

*Status: approved. Owner: role:ISMS-Manager. Next review: 2028-04-19.*

*Interim: legal signature pending QES integration. Approved via git-level only.*

## Context

ISO 27001 is the certification foundation. NISG 2026 is the domestic regulatory obligation. Impl Reg 2024/2690 is the NIS2 technical detail for specific sectors. GDPR Art. 32 overlaps materially and deserves first-class treatment. 27701 is natural next expansion but not required at v1.

## Decision

Version 1 in-scope frameworks: ISO/IEC 27001:2022, NISG 2026, Implementing Regulation (EU) 2024/2690, GDPR Art. 32. Structurally extensible to ISO/IEC 27701:2025; content deferred.

## Alternatives considered

Alternative 1: 27001 only. Rejected because NISG 2026 obligations exist regardless of 27001 scope.
Alternative 2: full regulatory scope (27001, 27701, 27017, 27018, 22301, NISG, GDPR, DORA, AI Act, CRA). Rejected as scope creep; defer multi-regulatory expansion to future phases.

## Consequences

Crosswalk in template/governance/controls/mapping.yaml is the single source of truth and extensible.

## Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | 2026-04-19 | approved | initial record |
