---
doc_id: REC-2026-001
doc_type: record
title: ISMS scope statement
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
  - iso27001:4.3
  - nisg2026:§34
signature_ref: null
---

# ISMS scope statement

**REC-2026-001 Revision 1 (DRAFT)**

*Status: draft. Owner: role:CISO. Next review: 2027-01-01.*

## 1. Entity

{{entity.legal_name}} ({{entity.short_name}}), {{entity.legal_form}}, Firmenbuch {{entity.register_number}}, located at {{entity.address.street}}, {{entity.address.postal_code}} {{entity.address.city}}, {{entity.address.country}}.

## 2. Jurisdiction and classification

Primary jurisdiction: {{entity.jurisdiction}}.

NISG 2026 classification: {{classification.nisg2026_category}}.

NISG 2026 sectors: {{classification.nisg2026_sectors}}.

GDPR role: {{classification.gdpr_role}}.

## 3. ISMS scope

{{scope.statement_summary}}

### 3.1 Locations in scope

{{scope.included_locations}}

### 3.2 Business units in scope

{{scope.included_business_units}}

### 3.3 Exclusions

{{scope.excluded_items}}

## 4. Interfaces and dependencies

TODO: interfaces to out-of-scope entities, cloud providers, service providers.

## 5. Related documents

- Interested parties: `governance/context/interested-parties.yaml`
- Internal and external issues: `governance/context/issues-internal-external.md`
- Information Security Policy: P-000
- Statement of Applicability: `governance/soa/soa.yaml`

## 6. Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | {{entity.draft_date}} | draft | initial draft |
