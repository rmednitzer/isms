---
doc_id: DEC-2026-004
doc_type: record
title: "Repo name isms"
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

# Repo name isms

**DEC-2026-004 Revision 1 - 2026-04-19**

*Status: approved. Owner: role:ISMS-Manager. Next review: 2028-04-19.*

*Interim: legal signature pending QES integration. Approved via git-level only.*

## Context

Generic name reflects the template-plus-instance design. Multi-jurisdiction capability is expressed in content (instance/config.yaml jurisdiction field, framework-refs registry) rather than name.

## Decision

The repository is named 'isms' (not 'isms-at' or 'isms-primary').

## Alternatives considered

Alternative 1: 'isms-at'. Rejected because Austrian primacy is already declared in content, and name-embedding would need change for any non-AT deployment.
Alternative 2: 'compliance-runtime' or similar. Rejected as less clear than 'isms' in describing what the repo is.

## Consequences

If a second parallel deployment is ever run, it gets its own repository with 'isms' equally valid as a base name; instance/config.yaml distinguishes them.

## Revision history

| Rev | Date | Status | Change |
|---|---|---|---|
| 1 | 2026-04-19 | approved | initial record |
