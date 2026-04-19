---
doc_id: DEC-2026-001
doc_type: record
title: "Standalone operation"
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

# Standalone operation

**DEC-2026-001 Revision 1 - 2026-04-19**

*Status: approved. Owner: role:ISMS-Manager. Next review: 2028-04-19.*

*Interim: legal signature pending QES integration. Approved via git-level only.*

## Context

Evidence must be reproducible by a future auditor cloning the repository. SaaS dependencies may change, deprecate, or vanish. Git plus a Python venv must suffice.

## Decision

This repository operates without runtime dependency on external services, skill stacks, or platform-specific AI tooling.

## Alternatives considered

Alternative 1: rely on commercial GRC platform for evidence storage. Rejected because platform dependency undermines reproducibility and introduces lock-in.
Alternative 2: rely on cloud-hosted AI assistant for validation. Rejected for the same reasons plus the asymmetric cost of the assistant being offline during audit.

## Consequences

Validators, core collectors, and packagers run offline. Optional collectors (law fetch, provider integrations) are gated behind explicit targets and must not break required operations on failure.

## Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | 2026-04-19 | approved | initial record |
