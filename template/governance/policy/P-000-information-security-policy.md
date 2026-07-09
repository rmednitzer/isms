---
doc_id: P-000
doc_type: policy
title: Information Security Policy
revision: 1
status: draft
approved_date: null
approved_by: null
owner: role:CISO
classification: public
supersedes_revision: null
next_review: 2027-01-01
language: en
framework_refs:
  - iso27001:5.2
  - iso27001:A.5.1
  - nisg2026:§31
  - implreg-2024-2690:Annex
signature_ref: null
---

# Information Security Policy

**P-000 Revision 1 (DRAFT)**

*Status: draft. Owner: role:CISO. Next review: 2027-01-01.*

## 1. Purpose

Top-level policy establishing management commitment, scope, roles, objectives.

## 2. Scope

Applies to {{entity.short_name}} and to all information, systems, personnel, and third parties within the ISMS scope per `governance/context/scope-statement.md`.

## 3. Policy statements
### 3.1 Principle

{{entity.short_name}} treats the confidentiality, integrity, and availability of
information as essential to its operations, its legal and regulatory obligations, and
the trust of its interested parties. Management establishes, maintains, and continually
improves an information security management system (ISMS) aligned with ISO/IEC
27001:2022.

### 3.2 Requirements

- The ISMS scope shall be defined and maintained in `governance/context/scope-statement.md`.
- Information security risks shall be assessed and treated through the risk management
  process, using the methodology in `governance/risk/methodology.md`.
- Controls shall be selected and applied per the Statement of Applicability
  (`governance/soa/soa.yaml`), covering the risk-management measures required by
  NISG 2026 § 31 and Implementing Regulation (EU) 2024/2690.
- Measurable information security objectives shall be set, monitored, and reviewed
  (`governance/objectives/isms-objectives.yaml`).
- Management shall provide the resources needed to operate and improve the ISMS and
  shall review it at planned intervals per ISO/IEC 27001 clause 9.3.
- Personnel and relevant third parties shall comply with this policy and its
  subordinate policies.

### 3.3 Prohibitions

- Information within the ISMS scope shall not be processed, stored, or transmitted
  outside approved systems and controls without a documented risk acceptance.
- Controls required by the Statement of Applicability shall not be disabled or
  circumvented.

### 3.4 Responsibilities

- The Leitungsorgan (role:Management) holds accountability for the ISMS and for the
  risk-management measures under NISG 2026 § 31.
- role:CISO and role:ISMS-Manager operate, monitor, and report on the ISMS.
- All personnel are responsible for adhering to this policy.

### 3.5 Exceptions

Deviations shall be documented, risk-assessed, and approved as a risk acceptance per
SOP-005. Exceptions shall carry an expiry date and shall be reviewed at management
review.

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
