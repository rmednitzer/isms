---
doc_id: DEC-2026-007
doc_type: record
title: "Asset register as governance record"
revision: 1
status: draft
approved_date: null
approved_by: null
owner: role:CISO
classification: internal
supersedes_revision: null
next_review: 2028-04-19
language: en
framework_refs:
  - iso27001:7.5.3
  - iso27002:A.5.9
signature_ref: null
---

# Asset register as governance record

**DEC-2026-007 Revision 1 (DRAFT)**

*Status: draft. Owner: role:CISO. Next review: 2028-04-19.*

## Context

ISO 27001 Annex A A.5.9 requires an inventory of information and other
associated assets. Most implementations conflate this with an operational
CMDB, producing either a too-detailed register that drifts from reality or a
too-shallow one that fails audit. The register's purpose for the ISMS is
distinct from an operational system of record.

## Decision

The asset register (and the companion facilities, network, and supplier
registers) is a governance record, not a CMDB. Fields are assurance-relevant:
owner role, custodian role, criticality, data classification, location
reference, network reference, supplier references, in-scope flag, lifecycle
status. Operational attributes (live IP assignments, depreciation,
ticket history, serial numbers beyond disposal evidence) stay in operational
systems. Register entries may point to those systems via a free-text
`operational_ref` field, but the register itself does not import them.

## Alternatives considered

- **Full CMDB with discovery.** Rejected. Import cadence and field drift would
  force the register to compete with the live operational system as a source
  of truth. Audit evidence needs a deliberate, curated, signed artefact.
- **Prose-only register.** Rejected. No schema, no validator coverage, no
  cross-register integrity, no path to the Selbstdeklaration package.

## Consequences

- Asset register entries are added and reviewed on a human cadence (quarterly
  per ET-CORE-002 through ET-CORE-006). Operational discovery tools may
  surface candidates for addition but do not write the register directly.
- Entries that become stale (system decommissioned, supplier terminated) are
  marked `lifecycle_status: retired` and remain in the register. Deletion is
  not the norm; the register carries history.
- The crossref validator enforces that references across registers and from
  the risk register resolve. This is the integrity evidence.

## Revision history

| Rev | Date       | Status | Change          |
|-----|------------|--------|-----------------|
| 1   | 2026-04-19 | draft  | initial record  |
