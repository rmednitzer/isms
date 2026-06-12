# Audit 03: Final report

Full audit, validation, hardening, and documentation pass. 2026-06-12.

## Executive summary

The repository is in good health. The baseline was already green (tests, lint,
types, and all nine governance validators pass), with no secrets in history and no
known dependency vulnerabilities. The audit found one notable security issue, a
shell and Python code-injection path in the human-evidence capture helper, and
fixed it with a regression test. It raised tooling test coverage from 78 % to
88 % by testing the validator entry points (the governance gates), and corrected a
documentation gap that made the documented build fail on Python 3.11. Remaining
findings are low or informational, structural (a dependency lockfile), or
authorisation-gated (CI workflow changes), and are recorded in `BACKLOG.md` with
proposed ADRs under `audit/adr/`.

No critical or high-severity issues were found. No behaviour was changed without a
test. No control-of-controls files (`.github/workflows/`, `CODEOWNERS`,
`.gitsigners`, role definitions) and no `instance/evidence/` files were modified.

## Baseline versus post-fix metrics

| Metric | Baseline | Post-fix |
|---|---|---|
| Tests | 102 passed | 113 passed |
| Coverage (tooling) | 78 % | 88 % |
| ruff (lint) | clean | clean |
| mypy | clean (42 files) | clean (44 files) |
| Validators | 9/9 pass | 9/9 pass |
| Secret scan (gitleaks, history) | no leaks | no leaks |
| Dependency vulnerabilities (pip-audit) | none | none |
| Validator coverage (bilingual / supersession / frontmatter) | 21 / 25 / 34 % | 90 / 94 / 91 % |

Findings by severity (12 total): critical 0, high 0, medium 4
(S-001, S-006, Q-001, Q-004), low 5 (S-002, S-004, S-007, Q-002, Q-005), info 3
(S-003, S-005, Q-003). Resolved this pass: S-001, S-002, Q-001, Q-002.

## Commits (oldest first)

| Commit | Rationale |
|---|---|
| `docs(audit):` phase 0-3 reports | Evidence: inventory, baseline, findings register (read-only) |
| `security:` capture.sh injection | Fix S-001 shell/Python code injection; add regression test |
| `chore:` ignore dist-audit-pack | Fix S-002; prevent confidential pack from being staged |
| `test:` validator main() paths | Fix Q-001; cover governance gates; coverage 78 % to 88 % |
| `docs:` Python 3.12+ prerequisite | Fix Q-002; align README and CLAUDE with the standalone charter |
| `docs:` audit ADRs | Backfill architecture/CI ADRs; forward proposals (0005-0007) |
| `docs:` remediation backlog | Consolidate deferred findings and proposals in BACKLOG.md |

Evidence collection (first commit) is kept separate from remediation, per the
brief. Every commit is signed (SSH signature; `gpgsig` header present).

## Deviations from the brief (with reasons)

- Branch: the brief suggested `audit/2026-06-12-full-pass`; the execution
  environment pins the session to `claude/affectionate-franklin-i5qu46`, which was
  used.
- ADR location: the brief asked for `docs/adr/` in MADR format. `docs/` is a scan
  root for `validate_frontmatter`, whose schema `status` enum lacks
  `proposed`/`accepted`, and the repository's canonical ADRs already live in
  `docs/decisions/DEC-*`. Audit ADRs were placed under `audit/adr/` to avoid
  breaking a validator and to avoid fabricating governance approvals. See
  `audit/adr/0001`.
- CI changes deferred: S-006 (dependency scanning) and the DCO restore (L8) require
  editing `.github/workflows/`, which is control-of-controls under the operating
  contract and needs separate human authorisation. They are proposed, not applied.
- Build environment: `make bootstrap` fails on this environment's Python 3.11
  (`requires-python >= 3.12`); dependencies were installed directly for
  measurement. CI uses Python 3.14 and is unaffected. Recorded as Q-002 and fixed
  in documentation.
- Tooling absent: semgrep and trufflehog were unavailable; SAST was a manual
  OWASP-oriented review and gitleaks covered secrets. pip-audit was installed and
  run. WeasyPrint was absent; the renderer was exercised via its HTML fallback.

## Residual risk statement

After this pass, no critical or high findings remain and the one code-injection
issue is closed and tested. Residual risk is concentrated in:

1. Supply-chain monitoring: dependencies are clean today but CI has no
   vulnerability gate (S-006) and there is no lockfile (Q-004), so reproducibility
   and ongoing CVE detection are weaker than the standalone charter implies.
2. Authorisation-gated items: S-006 and the DCO restore cannot be applied without a
   workflow change; until then DCO is not auto-enforced (L8).
3. Low and informational hardening opportunities (S-003, S-004, S-005, S-007) that
   are not externally reachable in the current, operator-run, no-network tooling.
4. Repository maturity: the ISMS is at skeleton state (LIMITATIONS L1); content
   depth, not tooling correctness, is the dominant open work.

The instance evidence chain, signature validation, YAML loading, PDF rendering,
and CI permission posture were reviewed and found sound (see
`audit/02-security-findings.md`, "Controls verified sound").

## Top 5 backlog items

1. S-006 Add dependency-vulnerability scanning to CI (medium, S, gated).
2. Q-004 Pin Python dependencies with a lockfile (medium, M).
3. Restore DCO auto-enforcement, LIMITATIONS L8 (medium, S, gated).
4. Q-005 Prune or gate unused runtime dependencies lxml/cryptography/dateutil
   (low, S, needs maintainer decision).
5. S-007 Validate the `--audit` argument in build_audit_pack (low, S).

Full list with owners and approaches: `BACKLOG.md`.
