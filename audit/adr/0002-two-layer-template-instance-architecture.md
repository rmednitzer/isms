# 0002. Two-layer template and instance architecture

- Status: accepted (backfill; decision already embodied in the repository)
- Date: 2026-06-12 (record written during the audit; the decision predates it)
- Deciders: original authors (rationale partly inferred, see below)

## Context

The repository must serve as both a reusable ISO 27001 / NISG 2026 framework and
one concrete organisational deployment, and must support further deployments
(client engagements, sister entities) without forking the framework.

## Decision

Separate a reusable `template/` layer (with `{{PLACEHOLDERS}}` and
`{{#if}}` blocks) from a per-deployment `instance/` layer, rendered by
`tooling/instantiate.py` from `instance/config.yaml`. Shared infrastructure
(`tooling/`, `framework-refs/`, `docs/`) sits beside both.

## Status of rationale

This decision is embodied in the code and documented operationally in
`README.md` ("Two-layer design"), `docs/operating-contract.md`, and
`docs/document-control.md` (the template-vs-instance boundary). It is not captured
as a standalone `DEC-YYYY-NNN`. The rationale above is reconstructed from those
documents and from `tooling/instantiate.py`; no rationale beyond what they state
is asserted here.

## Consequences

- A second deployment reuses `template/` and `tooling/` with a fresh `instance/`.
- The boundary is enforced only at render time; CI does not reject deployment
  content placed in the template layer (tracked as LIMITATIONS L2).
- `make instantiate` is idempotent; re-rendering on unchanged config is a no-op
  (verified: dry-run reported 163 files, no unresolved placeholders).

## Evidence

- `tooling/instantiate.py` (placeholder and conditional rendering, idempotent).
- `README.md` structure section; `docs/document-control.md` boundary definition.
- `examples/instance-acme/` as a worked second instance.
