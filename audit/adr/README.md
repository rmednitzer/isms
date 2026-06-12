# Architecture decision records (audit ADR index)

This directory holds ADRs produced by the 2026-06-12 audit pass, in MADR format
(https://adr.github.io/madr/).

## Note on location and format

The audit brief asked for `docs/adr/` in MADR format with `proposed`/`accepted`
status. Two repository facts make a literal reading impossible without breaking a
rule:

1. The repository already keeps its canonical, governed decision records under
   `docs/decisions/` as `DEC-YYYY-NNN` (per DOC-001). That is the project's ADR
   system.
2. `docs/` is a scan root for `validate_frontmatter`, whose front-matter schema
   `status` enum is `draft/under_review/approved/superseded/retired`. It does not
   include `proposed` or `accepted`. Authoring MADR files under `docs/` would
   either fail the validator (forbidden by the operating contract) or force MADR
   into the governance schema.

These audit ADRs therefore live under `audit/adr/` as audit work products. Any
proposal here that the maintainer accepts should be promoted into a governed
`DEC-YYYY-NNN` record under `docs/decisions/`.

## Canonical governed decisions (existing, authoritative)

See `docs/decisions/`:

| ID | Title |
|----|-------|
| DEC-2026-001 | Standalone operation |
| DEC-2026-002 | Two signature layers |
| DEC-2026-003 | Incident runbook outside merge pipeline |
| DEC-2026-004 | Repository name |
| DEC-2026-005 | Framework scope v1 |
| DEC-2026-006 | Cyber Trust Austria Platinum as candidate |
| DEC-2026-007 | Asset register as governance record |
| DEC-2026-008 | ISMS MCP overlay |

## Audit ADRs

| ID | Title | Status |
|----|-------|--------|
| 0001 | Use MADR for audit decision records | accepted |
| 0002 | Two-layer template and instance architecture | accepted (backfill) |
| 0003 | CI quality-gate strategy | accepted (backfill) |
| 0004 | Secure operator input in evidence capture | accepted |
| 0005 | Pin Python dependencies with a lockfile | proposed |
| 0006 | Prune unused runtime dependencies | proposed |
| 0007 | Dependency-vulnerability scanning in CI | proposed |

Backfill ADRs document decisions already embodied in the repository. Where the
original rationale is not recorded anywhere, that is stated rather than invented
(per the no-fabrication rule).
