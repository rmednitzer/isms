---
doc_id: PLAN-001
doc_type: plan
title: Risk assessment methodology
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
  - iso27001:6.1.2
  - iso27001:8.2
  - iso27001:8.3
signature_ref: null
---

# Risk assessment methodology

**PLAN-001 Revision 1 (DRAFT)**

*Status: draft. Owner: role:CISO. Next review: 2027-01-01.*

## 1. Purpose

Defines the methodology for identifying, analysing, evaluating, treating, and monitoring information security risks at {{entity.short_name}}, in conformance with ISO/IEC 27001:2022 clauses 6.1.2 and 8.2, aligned with ISO/IEC 27005.

## 2. Risk criteria

### 2.1 Risk acceptance criteria

Residual risks rated low may be accepted by role:ISMS-Manager. Residual risks rated medium require CISO acceptance. High and severe residual risks require Management (Leitungsorgan) acceptance.

### 2.2 Risk assessment criteria

Likelihood and impact are assessed on five-point scales; the combined rating is the risk level.

## 3. Likelihood scale

| Level | Label | Description |
|---|---|---|
| 1 | rare | may occur only in exceptional circumstances |
| 2 | unlikely | could occur at some time |
| 3 | possible | might occur at some time |
| 4 | likely | will probably occur in most circumstances |
| 5 | certain | is expected to occur in most circumstances |

## 4. Impact scale

| Level | Label | Description |
|---|---|---|
| 1 | negligible | insignificant business impact |
| 2 | minor | minor disruption, minor cost |
| 3 | moderate | localised disruption, material cost |
| 4 | major | service-wide disruption, significant financial or reputational cost |
| 5 | severe | existential threat, regulatory breach, critical service loss |

## 5. Risk matrix

| Impact | Rare | Unlikely | Possible | Likely | Certain |
|---|---|---|---|---|---|
| Severe | medium | high | high | severe | severe |
| Major | medium | medium | high | high | severe |
| Moderate | low | medium | medium | high | high |
| Minor | low | low | medium | medium | high |
| Negligible | low | low | low | medium | medium |

## 6. Risk treatment options

Accept, mitigate, transfer, avoid. Choice justified per risk in the treatment plan.

## 7. Cadence

Full risk reassessment: annually, and on material change to scope, threat landscape, or regulatory regime. Targeted reassessment: on incident, material supplier change, new service onboarding, or law change (per SOP-102).

## 8. Register and treatment plan

Identified risks recorded in `risk/register.yaml`; treatments in `risk/treatment-plan.yaml`; acceptances logged in `risk/acceptance-log.md`.

## 9. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | {{entity.draft_date}} | draft | initial draft |
