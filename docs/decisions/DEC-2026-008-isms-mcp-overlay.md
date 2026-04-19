---
doc_id: DEC-2026-008
doc_type: record
title: "Optional read-only ISMS MCP overlay"
revision: 1
status: draft
approved_date: null
approved_by: null
owner: role:ISMS-Manager
classification: internal
supersedes_revision: null
next_review: 2028-04-19
language: en
framework_refs:
  - iso27001:7.5.3
signature_ref: null
---

# Optional read-only ISMS MCP overlay

**DEC-2026-008 Revision 1 (DRAFT)**

*Status: draft. Owner: role:ISMS-Manager. Next review: 2028-04-19.*

## Context

A read-only Model Context Protocol server wraps the ISMS validators and
register loaders for consumption by AI clients (Claude Code, Claude
Desktop). It is implemented in a separate repository, `isms-mcp`,
installed as an optional developer tool.

## Decision

The overlay is permitted, provided:

1. It lives outside this repository.
2. It is never imported by, required by, or invoked from any code in
   `tooling/`, `Makefile`, or `.github/workflows/`.
3. It is read-only; no tool it exposes can commit, sign, modify evidence,
   or change control-of-controls files.
4. Its absence does not affect `make validate`, `make test`,
   `make currency-check`, `make pack`, or `make selbstdeklaration`.

## Alternatives considered

Alternative 1: embed the MCP server under `tooling/mcp/`. Rejected
because DOC-004 forbids runtime dependency on external skill stacks and
MCP servers, and the in-tree location would invite such dependency over
time.

Alternative 2: extend the existing Vertex MCP server with ISMS tools.
Rejected because Vertex is remote and ISMS content includes
`classification: restricted` items whose exposure over network transport
is a data-handling decision that deserves a distinct boundary.

## Consequences

- An auditor's clone plus `make bootstrap` reproduces all evidence
  without touching the overlay.
- Surveillance audit question "is there any external dependency" has a
  clean answer: no; the overlay is a convenience, not a link in the
  evidence chain.

## Revision history

| Rev | Date       | Status | Change          |
|-----|------------|--------|-----------------|
| 1   | 2026-04-19 | draft  | initial record  |
