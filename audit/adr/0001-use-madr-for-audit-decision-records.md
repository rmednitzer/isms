# 0001. Use MADR for audit decision records

- Status: accepted
- Date: 2026-06-12
- Deciders: audit pass (2026-06-12)

## Context

The audit pass needs to record architectural decisions: those already embodied in
the repository (backfill) and those proposed as a result of the audit (forward).
The repository's governed decision records live under `docs/decisions/` as
`DEC-YYYY-NNN` with schema-constrained front-matter and a formal approval
lifecycle. Audit proposals are not yet governance-approved, and MADR's
`proposed`/`accepted` vocabulary does not map onto the governance schema.

## Decision

Record audit ADRs under `audit/adr/` in MADR format. Keep `docs/decisions/` as the
single source of governed decisions. Promote any accepted proposal from
`audit/adr/` into a `DEC-YYYY-NNN` record through the normal governance flow.

## Consequences

- Audit proposals are visible and reviewable without entering the governed tree
  prematurely or fabricating an approval status.
- There are two ADR locations during the audit window; the index
  (`audit/adr/README.md`) states the relationship explicitly to avoid confusion.
- No validator is weakened and no governance approval is invented.
