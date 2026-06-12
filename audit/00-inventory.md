# Audit 00: Recon and inventory

Phase 0 of the full audit pass. Read-only. Generated 2026-06-12.

This document records the repository structure, toolchain actually available in
the audit environment, and the dependency surface. Every claim is backed by a
command run in this session; commands are quoted inline.

## Method

All commands run from the repository root on branch
`claude/affectionate-franklin-i5qu46` (the session branch; the task brief
suggested `audit/2026-06-12-full-pass`, but the execution environment pins the
session to the branch above, so that is used and noted here for traceability).

## Component map

The repository is a standalone Information Security Management System (ISMS)
framework plus tooling. It is documentation-heavy with a small Python tool layer.

| Area | Path | Contents |
|---|---|---|
| Repo operating rules | `docs/` | DOC-001..DOC-009 control documents, `docs/decisions/DEC-2026-001..008` decision records |
| Reusable framework | `template/` | `governance/`, `operations/`, `users/` with `{{PLACEHOLDERS}}` |
| One deployment | `instance/` | `config.yaml`, `governance/`, `operations/`, `evidence/` (append-only), `users/` |
| Law references | `framework-refs/` | `snapshots/`, `sources/registry.yaml`, `calendar/`, `currency/`, `impact-assessments/` |
| Tooling | `tooling/` | schemas, validators, collectors, signers, packagers, renderer, tests |
| Worked example | `examples/instance-acme/` | sample config, registers, sample policy |
| CI and ownership | `.github/` | workflows (ci, dco, reuse, scorecard), CODEOWNERS, issue/PR templates |
| Root scaffolding | repo root | README, CLAUDE, CONTRIBUTING, SECURITY, GOVERNANCE, LICENSE, NOTICE, REUSE.toml, CHANGELOG, STATUS, LIMITATIONS, EXTERNAL-READER-PROTOCOL, Makefile, renovate.json5, .pre-commit-config.yaml |

### Tooling breakdown

Command: `find tooling -type f` (filtered).

- `tooling/schemas/`: 18 JSON Schema files (frontmatter, soa, risk-register, attestation, incident, law-* and register schemas).
- `tooling/validators/`: 9 validators plus `_common.py` (frontmatter, crossrefs, signatures, supersession, law_references, calendar, bilingual, doc_type_coverage, registers).
- `tooling/collectors/core/`: 4 (control_coverage, evidence_age_report, inventory_from_repo, inventory_from_register).
- `tooling/collectors/optional/`: 7 (fetch_ris, fetch_eurlex, detect_delta, plus keycloak/openvas/veeam/wazuh stubs).
- `tooling/signers/`: 4 (sign_ssh, sign_gpg, qes_client_atrust, verify_qes).
- `tooling/packagers/`: 5 (render_pdf, build_audit_pack, build_soa_pdf, build_selbstdeklaration, build_management_review) plus Jinja2/CSS templates.
- `tooling/instantiate.py`, `tooling/capture.sh`.
- `tooling/tests/`: 12 test modules.

## Languages and size

Command: `git ls-files | sed 's/.*\.//' | sort | uniq -c | sort -rn`.

| Type | Tracked files |
|---|---|
| Markdown (`.md`) | 179 |
| Python (`.py`) | 42 |
| YAML (`.yaml`/`.yml`) | 41 |
| `.gitkeep` | 31 |
| JSON | 18 |
| Other (txt, toml, html, sh, json5, j2, css) | small counts |

Total tracked files: 327 (`git ls-files | wc -l`).
Python source lines: 3789 (`git ls-files '*.py' | xargs wc -l`).
The primary language by file count is Markdown (governance content); Python is
the only executable code layer.

## Build system and entry points

- Build/orchestration: GNU `Makefile` (GNU-only: pattern substitution and static
  pattern rules). Targets: `bootstrap`, `instantiate`, `validate`,
  `currency-check`, `snapshot-fetch`, `pack`, `selbstdeklaration`, `pdf`,
  `soa-pdf`, `test`, `clean`.
- Packaging: `tooling/pyproject.toml` (setuptools), package name `isms-tooling`,
  `requires-python = ">=3.12"`.
- Entry points are scripts invoked by the Makefile (validators, collectors,
  packagers, `instantiate.py`); there are no installed console-scripts.
- CLI surfaces: `instantiate.py` (`--config`, `--dry-run`, `--strict`),
  `render_pdf.py` (`source`, `--out`, `--html-only`, `--signature-block`,
  `--config`, `--generated-at`), `build_audit_pack.py` (`--audit`), signer CLIs.

## CI and supply-chain config

Command: `find .github -type f`; file reads.

- `.github/workflows/ci.yml`: Python 3.14, installs `tooling/[dev]`, runs ruff,
  mypy, `make test`, `make validate`. `permissions: contents: read`.
- `.github/workflows/dco.yml`: `workflow_dispatch` only (auto-trigger disabled;
  tracked as LIMITATIONS L8). `permissions: pull-requests: read`.
- `.github/workflows/reuse.yml`: REUSE 3.3 check. `permissions: contents: read`.
- `.github/workflows/scorecard.yml`: OSSF Scorecard, top-level `permissions:
  read-all`, job-level least privilege.
- All GitHub Actions are pinned by commit SHA with a version comment.
- `.pre-commit-config.yaml`: pre-commit-hooks v6.0.0 (trailing-whitespace,
  end-of-file-fixer, check-yaml, check-json, check-added-large-files,
  detect-private-key, no-commit-to-branch=main) and ruff-pre-commit v0.15.16.

No container, Kubernetes, Terraform, or systemd files are present
(`find` for Dockerfile/`*.tf`/`*.yaml` manifests returned none in scope).

## Dependency graph summary

Source: `tooling/pyproject.toml`.

- Direct runtime deps (7): `jsonschema>=4.21`, `ruamel.yaml>=0.18`,
  `python-dateutil>=2.8`, `requests>=2.31`, `lxml>=5.0`, `cryptography>=42.0`,
  `jinja2>=3.1`.
- Dev extras (6): `pytest>=8.0`, `pytest-cov>=5.0`, `ruff>=0.11`, `mypy>=1.10`,
  `types-jsonschema>=4.21`, `pre-commit>=3.7`.
- PDF extras (2): `markdown>=3.6`, `weasyprint>=62.0`.
- No JavaScript dependencies (no `package.json`).
- GitHub Actions deps: `actions/checkout`, `actions/setup-python`,
  `actions/upload-artifact`, `ossf/scorecard-action`,
  `github/codeql-action/upload-sarif`, `fsfe/reuse-action`,
  `tim-actions/get-pr-commits`, `tim-actions/dco` (all SHA-pinned).

### Lockfile state

No Python lockfile or pinned constraints file exists (`ls requirements*.txt`,
`pyproject.toml` show only floating lower bounds). Installs resolve to whatever
PyPI currently serves. `renovate.json5` enables lockfile maintenance, but there
is no lockfile for it to maintain on the Python side. This is recorded as a
reproducibility finding in `audit/02-security-findings.md` (Q-004), relevant to
the standalone-reproducibility charter (DEC-2026-001, `docs/standalone-charter.md`).

## Toolchain actually available in this environment

Command: version probes for each tool.

| Tool | Version | Notes |
|---|---|---|
| python3 | 3.11.15 | Below the project's `requires-python = ">=3.12"` |
| GNU Make | 4.3 | Satisfies the GNU-only Makefile |
| git | 2.43.0 | |
| ruff | 0.15.8 | System install |
| pytest | 9.0.3 | Installed into `.venv` for this audit |
| mypy | 2.1.0 | Installed into `.venv` for this audit |
| gpg | 2.4.4 | |
| gitleaks | present (dev build) | Used for secret scanning |
| node / npm | 22.22.2 / 10.9.7 | Not used by the project |
| semgrep | absent | SAST done manually (see Phase 2) |
| pip-audit | absent | Dependency audit done manually (see Phase 2) |
| trufflehog | absent | gitleaks used instead |
| weasyprint | absent | PDF render verified via `--html-only` fallback |

Note: the package index in this environment serves post-release versions (pip
26, pytest 9, mypy 2.1, cryptography 48, jsonschema 4.26). Versions above are the
actual resolved versions, recorded for reproducibility.

## Environment caveat (build)

`make bootstrap` fails in this environment because `requires-python = ">=3.12"`
rejects the available Python 3.11.15:

```text
ERROR: Package 'isms-tooling' requires a different Python: 3.11.15 not in '>=3.12'
```

CI uses Python 3.14, so CI is unaffected. For the audit, dependencies were
installed directly into the created `.venv` to bypass the editable-install
metadata gate. Validators and tests run because they locate modules via
`REPO_ROOT` and `sys.path` rather than the installed package. This is recorded as
Q-002 in the findings register and addressed by a documentation fix in Phase 5.
