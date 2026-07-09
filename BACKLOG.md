# Audit remediation backlog

Deferred items from the 2026-06-12 audit pass. Findings are defined in
`audit/02-security-findings.md`; decisions are in `audit/adr/`. Pre-existing scope
limits live in `LIMITATIONS.md` (L1 to L9) and are referenced, not duplicated.

Each item: finding ID, severity, effort (S/M/L), rationale, suggested approach,
dependencies, suggested owner role. Ordered by severity then effort within each
section.

Items resolved in this pass (not backlog): S-001, S-002 (security), Q-001
(test coverage), Q-002 (documentation). See `audit/03-final-report.md`.

Resolved subsequently: S-007 (`--audit` argument validation) is fixed in
`build_audit_pack.py` (`AUDIT_ARG_PATTERN`, rejects path-escape with exit 2)
with parametrized tests in `test_build_audit_pack.py`. S-004 (untested
symlink-refusal) now has a regression test in `test_tooling_fixes.py`.

## Security

### S-006 Add dependency-vulnerability scanning to CI
- Severity: medium. Effort: S. Owner: maintainer.
- Rationale: CI has no dependency CVE gate; a future vulnerable dependency would
  land unnoticed. A manual `pip-audit` this pass was clean.
- Approach: add a `pip-audit` (or `osv-scanner`) step to `.github/workflows/ci.yml`
  (audit ADR 0007).
- Dependencies: best paired with the lockfile item (Q-004 / ADR 0005) so the scan
  runs against a pinned set.
- Authorisation: changing `.github/workflows/` is control-of-controls and needs
  explicit, separate human authorisation.

### S-004 Close TOCTOU window in audit-pack symlink rejection
- Severity: low. Effort: M. Owner: maintainer.
- Rationale: `copytree_without_symlinks` scans for symlinks, then copies; a symlink
  introduced between check and copy is not re-checked.
- Approach: reject symlinks during the copy itself (custom `copy_function` or
  per-entry `os.walk(followlinks=False)`). Add a test.
- Dependencies: none.

### S-003 Filter markdown link URL schemes in the PDF renderer
- Severity: info. Effort: S. Owner: maintainer.
- Rationale: link hrefs are escaped but not scheme-filtered; inert in WeasyPrint
  PDF today, defence-in-depth only.
- Approach: allowlist `http`/`https`/`mailto`/relative; neutralise others. Add a
  test. Confirm `test_minimal_markdown_quotes_link_url` still holds.
- Dependencies: none.

### S-005 Constrain network fetcher hosts to an allowlist
- Severity: info. Effort: M. Owner: ISMS-Manager.
- Rationale: `fetch_ris.py`/`fetch_eurlex.py` fetch `authoritative_url` from the
  registry with no host allowlist (TLS and timeouts are already set).
- Approach: restrict to `ris.bka.gv.at` and `eur-lex.europa.eu`; reject other
  hosts. Changing the registry is already change-gated.
- Dependencies: none.

## Reliability

### Restore DCO auto-enforcement
- Reference: LIMITATIONS L8. Severity: medium. Effort: S. Owner: maintainer.
- Rationale: `dco.yml` is `workflow_dispatch` only, so sign-off is not enforced per
  PR.
- Approach: replay affected commits with matching `Signed-off-by`, then restore the
  `on: pull_request` trigger.
- Authorisation: changing `.github/workflows/` is control-of-controls.

### Refresh stale law snapshot AT.NISG-2026
- Reference: `validate_law_references` warning. Severity: low. Effort: S.
  Owner: ISMS-Manager.
- Rationale: snapshot age 26 days exceeds the 14-day cadence (non-fatal warning).
- Approach: `make snapshot-fetch` (network), diff, and classify any delta via
  SOP-102. Creating an impact assessment is confirmation-gated.
- Dependencies: network access.

## Quality

### Q-004 Pin Python dependencies with a lockfile
- Severity: medium. Effort: M. Owner: maintainer.
- Rationale: lower-bound-only deps and no lockfile undercut the standalone
  reproducibility contract (DEC-2026-001, `docs/standalone-charter.md`).
- Approach: `pip-compile`/`uv lock`; consume from bootstrap and CI; let Renovate
  maintain it (audit ADR 0005).
- Dependencies: enables S-006.

### Q-005 Prune or gate unused runtime dependencies
- Severity: low. Effort: S. Owner: maintainer.
- Rationale: `lxml`, `cryptography`, `python-dateutil` are declared but never
  imported (audit ADR 0006).
- Approach: remove from runtime deps, or move behind an extra with a comment if
  reserved for planned work.
- Dependencies: maintainer decision on whether they are reserved.

### Raise coverage on remaining tooling paths
- Severity: low. Effort: S. Owner: maintainer.
- Rationale: `instantiate.py` (55 %) and `validate_crossrefs.py` (76 %) retain
  untested branches after this pass lifted the total to 88 %.
- Approach: add tests for `instantiate.render_tree` strict/unresolved paths and the
  crossrefs register-resolution failure branch.

## Documentation

### Pre-existing documentation limits
- Reference: LIMITATIONS L2 (template/instance boundary CI check), L5 (drift-watch
  registry), L6 (per-file SPDX retrofit). Owner: ISMS-Manager.
- These remain tracked in `LIMITATIONS.md`; no audit action beyond noting they are
  current.

### Add examples/ to the README structure tree
- Severity: info. Effort: S. Owner: maintainer.
- Rationale: the `README.md` structure diagram omits `examples/`, which the entry
  points table references.
- Approach: add one line to the structure block.

## Tooling

### Pre-check Python version in `make bootstrap`
- Severity: low. Effort: S. Owner: maintainer.
- Rationale: on Python < 3.12 bootstrap fails with an opaque pip metadata error
  (Q-002 documented, but the UX remains poor).
- Approach: a Makefile guard that checks the interpreter version and prints a clear
  message before attempting the install. Behaviour change, so add a test.
- Dependencies: none.
