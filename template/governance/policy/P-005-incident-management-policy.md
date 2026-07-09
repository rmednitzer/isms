---
doc_id: P-005
doc_type: policy
title: Incident Management Policy
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
  - iso27002:A.5.24
  - iso27002:A.5.25
  - iso27002:A.5.26
  - iso27002:A.5.27
  - iso27002:A.5.28
  - nisg2026:§32
signature_ref: null
---

# Incident Management Policy

**P-005 Revision 1 (DRAFT)**

*Status: draft. Owner: role:CISO. Next review: 2027-01-01.*

## 1. Purpose

Incident management lifecycle; NIS2 incident reporting obligations.

## 2. Scope

Applies to {{entity.short_name}} and to all information, systems, personnel, and third parties within the ISMS scope per `governance/context/scope-statement.md`.

## 3. Policy statements
### 3.1 Principle

Information security events shall be reported, assessed, and responded to through a
defined incident-management process that limits harm and meets the incident-reporting
obligations under NISG 2026 § 32 (A.5.24).

### 3.2 Requirements

- Incident management responsibilities and procedures shall be established and maintained
  (A.5.24; procedure SOP-001).
- Events shall be assessed and classified to decide whether they are incidents (A.5.25).
- Incidents shall be responded to and evidence collected per the procedures
  (A.5.26, A.5.28).
- Reportable incidents shall be notified to CERT.at and the Bundesamt within the NIS2
  windows: Frühwarnung within 24 hours, notification within 72 hours, final report within
  one month.
- Lessons learned shall be used to reduce the likelihood and impact of future incidents
  (A.5.27).

### 3.3 Prohibitions

- Incident evidence shall not be altered or deleted; handling shall preserve chain of
  custody.
- Authority notifications shall not be submitted by automated tooling; the accountable
  human submits them per the operating contract.

### 3.4 Responsibilities

- role:CISO leads incident response; role:ISMS-Manager coordinates reporting;
  role:Management approves external notifications.

### 3.5 Exceptions

There are no exceptions to statutory reporting obligations. Procedural deviations shall
be recorded in the incident record.

## 4. Roles and responsibilities

Per `users/roles.yaml`. Key accountability: role:CISO.

## 5. Related documents

- Parent policy: `governance/policy/P-000-information-security-policy.md`
- Supporting procedures: SOP references to be added as they are drafted.
- Supporting standards: STD references to be added as they are drafted.

## 6. Compliance

Non-compliance is addressed per the applicable disciplinary procedure. Exceptions require risk acceptance per SOP-005.

## 7. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | {{entity.draft_date}} | draft | initial draft |
