---
doc_id: P-006
doc_type: policy
title: Business Continuity Policy
revision: 1
status: draft
approved_date: null
approved_by: null
owner: role:CISO
classification: internal
supersedes_revision: null
next_review: 2027-01-01
language: en
framework_refs:
  - iso27002:A.5.29
  - iso27002:A.5.30
  - iso27002:A.8.13
  - iso27002:A.8.14
signature_ref: null
---

# Business Continuity Policy

**P-006 Revision 1 (DRAFT)**

*Status: draft. Owner: role:CISO. Next review: 2027-01-01.*

## 1. Purpose

Business continuity during disruption; ICT readiness; backup.

## 2. Scope

Applies to {{entity.short_name}} and to all information, systems, personnel, and third parties within the ISMS scope per `governance/context/scope-statement.md`.

## 3. Policy statements
### 3.1 Principle

{{entity.short_name}} shall maintain the capability to continue and recover critical
activities and ICT services at agreed levels during and after a disruption
(A.5.29, A.5.30).

### 3.2 Requirements

- Continuity requirements shall be derived from a business impact analysis defining MTPD,
  RTO, and RPO per critical service (`governance/dr-bcp/bia.yaml`).
- ICT readiness for business continuity shall be planned, implemented, and tested
  (A.5.30).
- Information shall be backed up and restore tests performed on a defined cadence (A.8.13).
- Processing facilities shall be implemented with the redundancy needed to meet
  availability requirements (A.8.14).
- Continuity and recovery arrangements shall be exercised at planned intervals and after
  significant change.

### 3.3 Prohibitions

- Backups shall not be treated as valid until a successful restore test is recorded.

### 3.4 Responsibilities

- role:ISMS-Manager owns the continuity plan; role:SysAdmin operates backup and recovery;
  role:Management approves the business impact analysis.

### 3.5 Exceptions

Exceptions shall be risk-accepted per the risk acceptance process (`governance/risk/methodology.md`, logged in `governance/risk/acceptance-log.md`) with a remediation date.

## 4. Roles and responsibilities

Per `users/roles.yaml`. Key accountability: role:CISO.

## 5. Related documents

- Parent policy: `governance/policy/P-000-information-security-policy.md`
- Supporting procedures: SOP references to be added as they are drafted.
- Supporting standards: STD references to be added as they are drafted.

## 6. Compliance

Non-compliance is addressed per the applicable disciplinary procedure. Exceptions require risk acceptance per the risk acceptance process (`governance/risk/methodology.md`, logged in `governance/risk/acceptance-log.md`).

## 7. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | {{entity.draft_date}} | draft | initial draft |
