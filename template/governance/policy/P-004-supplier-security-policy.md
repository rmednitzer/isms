---
doc_id: P-004
doc_type: policy
title: Supplier Security Policy
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
  - iso27002:A.5.19
  - iso27002:A.5.20
  - iso27002:A.5.21
  - iso27002:A.5.22
  - iso27002:A.5.23
  - nisg2026:§31
signature_ref: null
---

# Supplier Security Policy

**P-004 Revision 1 (DRAFT)**

*Status: draft. Owner: role:ISMS-Manager. Next review: 2027-01-01.*

## 1. Purpose

Information security in supplier relationships; supply-chain obligations per NIS2.

## 2. Scope

Applies to {{entity.short_name}} and to all information, systems, personnel, and third parties within the ISMS scope per `governance/context/scope-statement.md`.

## 3. Policy statements
### 3.1 Principle

Information security risks arising from supplier and service-provider relationships shall
be identified, agreed, and managed throughout the relationship lifecycle, including
supply-chain obligations under NIS2 / NISG 2026 § 31 (A.5.19).

### 3.2 Requirements

- Security requirements shall be agreed with suppliers before access is granted and
  documented in contracts or data-processing agreements (A.5.20).
- Risks in the ICT supply chain shall be assessed and managed (A.5.21).
- Supplier service delivery shall be monitored and reviewed, and changes managed against
  agreed requirements (A.5.22).
- Security requirements for cloud services shall be defined before adoption (A.5.23).
- Suppliers shall be recorded in the supplier register with criticality and review dates.

### 3.3 Prohibitions

- Suppliers shall not be granted access to information or systems before security
  requirements are agreed.

### 3.4 Responsibilities

- role:ISMS-Manager maintains the supplier register and review cadence; asset and service
  owners sponsor supplier relationships.

### 3.5 Exceptions

Exceptions shall be risk-accepted per SOP-005 with an expiry date.

## 4. Roles and responsibilities

Per `users/roles.yaml`. Key accountability: role:ISMS-Manager.

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
