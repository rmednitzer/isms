# 0003. CI quality-gate strategy

- Status: accepted (backfill; decision already embodied in the repository)
- Date: 2026-06-12 (record written during the audit; the decision predates it)
- Deciders: original authors (rationale partly inferred, see below)

## Context

A governance repository must keep its tooling correct and its supply chain
auditable, while remaining standalone (no required network at validate/pack time).

## Decision

Gate every pull request with GitHub Actions running, in order: ruff lint, mypy
type check, `make test` (pytest), and `make validate` (the nine offline
validators). Add REUSE 3.3 licensing compliance and OSSF Scorecard as separate
workflows. Pin every action by commit SHA and set least-privilege `permissions:`
blocks per workflow.

## Status of rationale

The decision is embodied in `.github/workflows/` and summarised in
`CONTRIBUTING.md`. There is no standalone `DEC-YYYY-NNN`. The rationale is
reconstructed from those files; nothing beyond what they show is asserted.

## Consequences

- Correctness, typing, tests, and governance validators all block merge.
- Supply-chain posture is strong: SHA-pinned actions, scoped tokens, Scorecard.
- There is no dependency-vulnerability scan step (see audit ADR 0007, finding
  S-006) and DCO auto-enforcement is currently disabled (LIMITATIONS L8).
- CI runs on Python 3.14 while the project declares `requires-python >= 3.12`;
  local clones on 3.11 cannot bootstrap (finding Q-002, fixed in docs this pass).

## Evidence

- `.github/workflows/ci.yml`, `reuse.yml`, `scorecard.yml` (read during audit).
- `permissions: contents: read` on ci/reuse; least-privilege job scopes on
  scorecard; all `uses:` pinned by SHA with version comments.
