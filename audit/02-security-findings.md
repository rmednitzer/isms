# Audit 02: Security and code-quality findings register

Phases 2 and 3 of the full audit pass. Read-only analysis. Generated 2026-06-12.

Security findings are prefixed `S-`; code-quality findings are prefixed `Q-`.
Severity scale: critical, high, medium, low, info. Effort scale: S, M, L.
Every finding cites a file location and the command or read that produced the
evidence. Where a property could not be verified in this environment it is marked
`[UNVERIFIED]`.

## Method and tool availability

| Activity | Tool | Status |
|---|---|---|
| Secret scan (history) | gitleaks `detect` | Run: 53 commits, no leaks |
| Secret scan (tree) | gitleaks `--no-git` | Run: 4 hits, all inside locally created `.venv/` (cryptography package stubs), none in tracked files |
| Dependency vulnerabilities | pip-audit 2.10.1 | Run: no known vulnerabilities found |
| SAST | semgrep | Absent; manual OWASP-oriented review performed |
| XML parsing review (XXE) | manual | No XML parsing exists in code |
| IaC review | manual | No Dockerfile/K8s/Terraform/systemd present |

The secret scans confirm the repository is clean: `gitleaks detect` over the full
history reported `no leaks found`; the 4 working-tree hits are in the audit's own
`.venv/` and are not tracked (`.venv/` is git-ignored).

## Findings summary

| ID | Title | Severity | Effort |
|---|---|---|---|
| S-001 | Shell and Python code injection in `tooling/capture.sh` | medium | M |
| S-002 | `dist-audit-pack/` build output not git-ignored (confidential leak risk) | low | S |
| S-003 | Markdown link URL scheme not filtered in renderer | info | S |
| S-004 | TOCTOU window in audit-pack symlink rejection | low | M |
| S-005 | Network fetchers accept registry URLs with no host allowlist | info | M |
| S-006 | No dependency-vulnerability scan step in CI | medium | S |
| S-007 | `build_audit_pack.py --audit` flows unsanitised into output path | low | S |
| Q-001 | Validator `main()` entry points are largely untested | medium | M |
| Q-002 | Bootstrap requires Python 3.12+ but this is undocumented; fails on 3.11 | low | S |
| Q-003 | Defensive broad `except Exception` blocks (reviewed, acceptable) | info | n/a |
| Q-004 | No Python lockfile; floating versions undercut reproducibility charter | medium | M |
| Q-005 | Three declared runtime dependencies are unused | low | S |

## Security findings

### S-001 Shell and Python code injection in tooling/capture.sh

- Severity: medium. CWE-78 (OS command injection), CWE-94 (code injection).
- Location: `tooling/capture.sh:40-53` (heredoc) and `tooling/capture.sh:61-70`
  (Python snippet).
- Evidence: file read. The attestation YAML is written with an unquoted heredoc
  `cat > "${ATT_PATH}" <<EOF`, so shell parameter expansion and command
  substitution run on the interpolated field values (`SOURCE_SYSTEM`,
  `SOURCE_INSTANCE`, and the reviewer `NOTES` taken from stdin). Separately, the
  per-attachment loop builds a Python program by string-interpolating
  `${ATT_PATH}`, `${base}` (an attachment file basename), and `${sha}` directly
  into Python string literals passed to `python3 -c`.
- Exploit plausibility: an evidence attachment whose filename contains a single
  quote or a Python expression breaks out of the `-c` string literal and executes
  Python as the operator. A reviewer note (or source-system field) pasted from an
  untrusted source that contains `$(...)` or backticks is command-substituted by
  the shell while the heredoc is written. The tool is operator-run, so this is not
  a remote surface, but evidence filenames and pasted notes are routinely
  attacker-influenced data in an incident-handling context.
- Recommended fix: quote the heredoc delimiter (`<<'EOF'`) and inject all dynamic
  values through a small Python helper that receives them via environment
  variables or argv (never via string interpolation), building the YAML with
  ruamel. Add a shell-level test that an attachment named with a single quote does
  not execute code.
- Fix effort: M.

### S-002 dist-audit-pack/ build output not git-ignored

- Severity: low. CWE-200 / CWE-538 (exposure of sensitive information in a file).
- Location: `.gitignore` (absent entry); `tooling/packagers/build_audit_pack.py:26`.
- Evidence: `.gitignore` ignores `dist/` but not `dist-audit-pack/`; running
  `make pack AUDIT=stage-1` left `?? dist-audit-pack/` in `git status`. The pack
  copies `instance/evidence/` and rendered governance, which are confidential to
  the deploying organisation (per `docs/document-control.md`).
- Exploit plausibility: a `git add -A` after building a pack would stage
  confidential instance evidence into the framework repository. Requires an
  operator mistake; not externally reachable.
- Recommended fix: add `dist-audit-pack/` to `.gitignore`.
- Fix effort: S.

### S-003 Markdown link URL scheme not filtered in renderer

- Severity: info. CWE-79 (theoretical only).
- Location: `tooling/packagers/render_pdf.py:120-123` (`_inline`).
- Evidence: link hrefs from markdown are HTML-escaped but their scheme is not
  validated, so `[x](javascript:...)` or `data:` URIs pass through into the HTML.
- Exploit plausibility: none in the current pipeline. WeasyPrint produces a PDF
  and does not execute JavaScript, and the resource fetcher
  (`_make_url_fetcher`) already blocks `http/https/ftp` and confines `file://` to
  the repository. The href is also HTML-attribute-escaped. Recorded for
  defence-in-depth only.
- Recommended fix: allowlist link schemes (`http`, `https`, `mailto`, relative)
  and drop or neutralise others; add a unit test.
- Fix effort: S.

### S-004 TOCTOU window in audit-pack symlink rejection

- Severity: low. CWE-367 (time-of-check to time-of-use).
- Location: `tooling/packagers/build_audit_pack.py:29-37`
  (`copytree_without_symlinks`).
- Evidence: the function walks `src.rglob("*")` rejecting symlinks, then calls
  `shutil.copytree`. A symlink introduced between the scan and the copy would not
  be re-checked.
- Exploit plausibility: requires a local concurrent writer during pack build;
  operator-run, single-user context. Low.
- Recommended fix: reject symlinks during the copy itself (custom `copy_function`
  or `os.walk(followlinks=False)` with per-entry checks), not only beforehand.
- Fix effort: M.

### S-005 Network fetchers accept registry URLs with no host allowlist

- Severity: info. CWE-918 (theoretical only).
- Location: `tooling/collectors/optional/fetch_ris.py:62`,
  `tooling/collectors/optional/fetch_eurlex.py:60`.
- Evidence: `authoritative_url` is read from
  `framework-refs/sources/registry.yaml` and fetched with `requests.get`.
  Timeouts are set (`timeout=60`) and TLS verification is left at the secure
  default. There is no allowlist restricting the host.
- Exploit plausibility: low. The registry is operator-controlled and changing it
  requires explicit human confirmation per the repository's own rules; these
  collectors are invoked only by the explicit `make snapshot-fetch` target.
- Recommended fix: constrain fetch hosts to a small allowlist (ris.bka.gv.at,
  eur-lex.europa.eu) and reject other hosts.
- Fix effort: M.

### S-006 No dependency-vulnerability scan step in CI

- Severity: medium. CWE-1104 (use of unmaintained/again-unscanned components),
  process gap.
- Location: `.github/workflows/ci.yml` (no audit step).
- Evidence: CI runs ruff, mypy, tests, validators, REUSE, and Scorecard, but no
  `pip-audit`/`osv-scanner` step. A manual `pip-audit` run during this audit found
  no known vulnerabilities, but nothing keeps that true over time.
- Exploit plausibility: not a direct vulnerability; a monitoring gap that lets a
  future vulnerable dependency land unnoticed.
- Recommended fix: add a `pip-audit` step to CI. Note: `.github/workflows/` is a
  control-of-controls path requiring separate human authorisation, so this is
  deferred to the backlog rather than changed in this pass.
- Fix effort: S (deferred; authorisation-gated).

### S-007 build_audit_pack.py --audit flows unsanitised into output path

- Severity: low. CWE-22 (path traversal).
- Location: `tooling/packagers/build_audit_pack.py:46`
  (`out = DIST / f"{args.audit}-{stamp}"`).
- Evidence: the `--audit` value is concatenated into the output directory path
  without validation. A value containing `../` would direct the pack outside
  `dist-audit-pack/`.
- Exploit plausibility: low. Operator-supplied via `make pack AUDIT=...`; the
  README documents a fixed set of audit stages.
- Recommended fix: validate `--audit` against a pattern (for example
  `^[A-Za-z0-9-]+$`) or an allowlist of known stages; reject otherwise.
- Fix effort: S.

## Code-quality findings

### Q-001 Validator main() entry points are largely untested

- Severity: medium. Effort: M.
- Location: `tooling/validators/validate_bilingual.py` (21 % cov),
  `validate_supersession.py` (25 %), `validate_frontmatter.py` (34 %),
  `validate_crossrefs.py` (45 %).
- Evidence: coverage report (Phase 1). Tests exercise helper functions but not the
  `main()` file-walk paths, which are the actual governance gates that CI relies on.
- Recommended fix: add tests that run each validator `main()` against a small
  fixture tree (a passing case and a failing case) asserting exit codes.
- Note: these validators are the enforcement surface for Hard Rule 4; untested
  `main()` paths mean a regression could silently weaken enforcement.

### Q-002 Bootstrap requires Python 3.12+ but this is undocumented

- Severity: low. Effort: S.
- Location: `tooling/pyproject.toml` (`requires-python = ">=3.12"`), `README.md`
  Quickstart, `CLAUDE.md` pre-flight check 3.
- Evidence: `make bootstrap` fails on Python 3.11.15 with
  `requires a different Python: 3.11.15 not in '>=3.12'`. Neither the README
  Quickstart nor the CLAUDE pre-flight states the minimum interpreter version.
- Recommended fix: document the Python 3.12+ requirement in the README Quickstart
  and the CLAUDE pre-flight; optionally have `make bootstrap` print a clear
  version-gate message.

### Q-003 Defensive broad except Exception blocks (reviewed, acceptable)

- Severity: info. Effort: n/a (no action recommended).
- Location: `validate_crossrefs.py:114` (import fallback with WARNING),
  `fetch_ris.py:135` / `fetch_eurlex.py:130` (per-source failure isolation in a
  loop that counts and reports), `inventory_from_repo.py:28` /
  `inventory_from_register.py:37` (git subprocess fallback).
- Evidence: file reads. Each broad catch is a deliberate resilience boundary that
  logs and degrades gracefully rather than masking a programming error.
- Recommendation: none. Recorded to show the pattern was examined.

### Q-004 No Python lockfile; floating versions undercut the reproducibility charter

- Severity: medium. Effort: M.
- Location: `tooling/pyproject.toml` (lower-bound-only deps), repository root (no
  lockfile), `renovate.json5` (enables lockfile maintenance).
- Evidence: there is no `requirements*.txt`, no `*.lock`, no pinned constraints.
  Installs resolve to whatever PyPI serves (this audit observed pip 26, mypy 2.1,
  cryptography 48). `docs/standalone-charter.md` and DEC-2026-001 make
  "an auditor's clone plus `make bootstrap` reproduces all evidence" a contract;
  floating versions weaken that contract.
- Recommended fix: add a pinned constraints/lock file (for example
  `pip-compile`/`uv lock`) consumed by `make bootstrap` and CI.

### Q-005 Three declared runtime dependencies are unused

- Severity: low. Effort: S.
- Location: `tooling/pyproject.toml` dependencies.
- Evidence: `grep` for imports shows `lxml`, `cryptography`, and
  `python-dateutil` are imported in zero source files; only `ruamel.yaml`,
  `jsonschema`, `jinja2`, and `requests` are used. `lxml` and `cryptography` are
  large compiled packages with their own CVE histories.
- Exploit plausibility: increases install footprint and attack surface for no
  current benefit.
- Recommended fix: remove the three from runtime dependencies, or, if they are
  reserved for planned work (`cryptography` for QES, `lxml` for EUR-Lex XML
  parsing, `python-dateutil` for date math), move them behind an extra and add a
  comment. This needs a maintainer decision on intent, so it is proposed in the
  backlog rather than changed unilaterally.

## Controls verified sound (negative results)

These were checked and found robust; recorded so the register is not read as a
list of only weaknesses.

- No secrets in history or tracked tree (gitleaks, 53 commits).
- No known dependency vulnerabilities (pip-audit 2.10.1).
- No unsafe deserialization: every YAML load uses ruamel `YAML(typ="safe")` or
  `typ="rt")`; neither executes arbitrary Python (unlike PyYAML `yaml.load`).
- No XML parsing, so no XXE surface.
- Signing wrappers (`sign_ssh.py`, `sign_gpg.py`) use list-argument
  `subprocess.check_call` with no `shell=True`; no shell-injection surface.
- The PDF renderer blocks external resource loading and confines `file://` URLs to
  the repository (`render_pdf.py:_make_url_fetcher`), and escapes raw HTML in
  markdown bodies. Covered by `test_url_fetcher_blocks_external_and_out_of_repo_file`.
- `validate_signatures.py` confines `signature_ref` to
  `instance/evidence/signatures/` via `is_relative_to`, requires the `%PDF` magic,
  and rejects empty or absolute references (defends Hard Rule 3).
- CI workflows set least-privilege `permissions:` blocks and pin every GitHub
  Action by commit SHA.
- No TLS verification is disabled anywhere (`verify=False` absent); network calls
  set timeouts.

## External input boundary enumeration

| Boundary | Surface | Validation posture |
|---|---|---|
| CLI args | `instantiate.py`, `render_pdf.py`, `build_audit_pack.py`, signers | argparse typed; `--audit` unsanitised into path (S-007); `--generated-at` parsed safely |
| Config files | `instance/config.yaml`, `framework-refs/sources/registry.yaml` | ruamel safe/rt load; operator-controlled, change-gated |
| Markdown front-matter | governance `.md` | schema-validated (frontmatter.schema.json); raw HTML escaped on render |
| Markdown body | governance `.md` | minimal converter escapes HTML; link scheme unfiltered (S-003) |
| Attachment filenames | `capture.sh` argv | interpolated unsafely into shell/Python (S-001) |
| Operator stdin | `capture.sh` notes/fields | interpolated into unquoted heredoc (S-001) |
| Network responses | `fetch_ris.py`, `fetch_eurlex.py` | written to snapshot files; host not allowlisted (S-005); TLS+timeout OK |
| Environment variables | none read in code | no secret resolution in tooling (consistent with stub collectors) |
| Network listeners | none | no servers, no webhook handlers in tooling |

## Remediation routing (input to Phase 4)

- Fix in this pass (safe, local, with tests): S-001, S-002, S-003, S-007, Q-001.
- Documentation fix (Phase 5): Q-002.
- Backlog (authorisation-gated or structural): S-004, S-005, S-006 (touches
  `.github/workflows/`, control-of-controls), Q-004, Q-005.
