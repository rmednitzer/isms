---
doc_id: P-011
doc_type: policy
title: Logging and Monitoring Policy
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
  - iso27002:A.8.15
  - iso27002:A.8.16
  - iso27002:A.8.17
signature_ref: null
---

# Logging and Monitoring Policy

**P-011 Revision 1 (DRAFT)**

*Status: draft. Owner: role:ISMS-Manager. Next review: 2027-01-01.*

## 1. Purpose

Logging, monitoring, clock synchronisation for security events.

## 2. Scope

Applies to {{entity.short_name}} and to all information, systems, personnel, and third parties within the ISMS scope per `governance/context/scope-statement.md`.

## 3. Policy statements
### 3.1 Principle

Security-relevant events shall be logged, protected, and monitored to detect anomalous
activity and support investigation (A.8.15).

### 3.2 Requirements

- Logs recording user activities, exceptions, faults, and security events shall be
  produced, retained, and protected against tampering (A.8.15).
- Networks, systems, and applications shall be monitored for anomalous behaviour and
  appropriate action taken (A.8.16).
- Clocks shall be synchronised to an approved time source to support correlation (A.8.17).
- Log retention shall meet the configured retention period and applicable legal
  requirements.

### 3.3 Prohibitions

- Logs shall not be modified or deleted before the end of their retention period.
- Logging of security events shall not be disabled on in-scope systems.

### 3.4 Responsibilities

- role:CISO defines monitoring requirements; role:SysAdmin operates logging, monitoring,
  and time synchronisation.

### 3.5 Exceptions

Exceptions shall be risk-accepted per the risk acceptance process (`governance/risk/methodology.md`, logged in `governance/risk/acceptance-log.md`) with a remediation date.

## 4. Roles and responsibilities

Per `users/roles.yaml`. Key accountability: role:ISMS-Manager.

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
