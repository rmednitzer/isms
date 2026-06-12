# Audit 01: Validation baseline

Phase 1 of the full audit pass. Read-only. Generated 2026-06-12.

This baseline is the regression reference for every later change. All numbers come
from commands run in this session and quoted below. Where a documented workflow
could not be run as written, the deviation is recorded explicitly.

## Clean-state build

Documented command: `make bootstrap`.

Result: FAIL in this environment.

```text
python3 -m venv .venv                       # ok
.venv/bin/python -m pip install --upgrade pip   # ok (pip 26.1.2)
.venv/bin/python -m pip install -e "tooling/[dev]"
ERROR: Package 'isms-tooling' requires a different Python: 3.11.15 not in '>=3.12'
make: *** [Makefile:29: bootstrap] Error 1   (exit 2)
```

Cause: `tooling/pyproject.toml` `requires-python = ">=3.12"`; the environment has
Python 3.11.15. CI pins Python 3.14, so CI is not affected. This is a real local
build break for any clone on Python 3.11. Recorded as Q-002.

Workaround used for the rest of the baseline: install the declared dependencies
directly into `.venv` (the package code itself imports cleanly on 3.11). This is a
measurement workaround, not a repository change.

```shell
.venv/bin/python -m pip install "jsonschema>=4.21" "ruamel.yaml>=0.18" \
  "python-dateutil>=2.8" "requests>=2.31" "lxml>=5.0" "cryptography>=42.0" \
  "jinja2>=3.1" "pytest>=8.0" "pytest-cov>=5.0" "mypy>=1.10" "types-jsonschema>=4.21"
# Successfully installed ... (exit 0)
```

## Test suite

Command: `.venv/bin/python -m pytest tooling/tests`.

| Metric | Value |
|---|---|
| Result | PASS |
| Passed | 102 |
| Failed | 0 |
| Skipped | 0 |
| Runtime | 0.71 s |
| Exit code | 0 |

No flaky candidates observed (single fast run; deterministic unit tests with no
network, no sleeps, no time-of-day logic except where `--generated-at` is injected
for reproducibility). Test modules: 12, covering schemas, frontmatter, crossrefs,
registers, supersession, bilingual, instantiate, renderer, render_pdf,
config-schema.

## Coverage

Command: `.venv/bin/python -m pytest tooling/tests --cov=tooling --cov-report=term-missing`.

Total coverage: 78 percent (1280 statements, 277 missed).

Lowest-covered non-test modules:

| Module | Coverage | Note |
|---|---|---|
| `validators/validate_bilingual.py` | 21 % | `main()` and file-walk untested |
| `validators/validate_supersession.py` | 25 % | `main()` and file-walk untested |
| `validators/validate_frontmatter.py` | 34 % | `main()` untested |
| `validators/validate_crossrefs.py` | 45 % | `main()` largely untested |
| `instantiate.py` | 55 % | `render_tree`/`main` partially untested |
| `validators/validate_registers.py` | 73 % | |
| `packagers/render_pdf.py` | 86 % | well covered |

Tests exercise helper functions thoroughly but not the validator `main()` entry
points, which are the actual governance gates. Recorded as Q-001.

## Linters, formatters, type checkers (check-only)

| Tool | Command | Result | Exit |
|---|---|---|---|
| ruff (lint) | `ruff check tooling/ --config tooling/pyproject.toml` | All checks passed | 0 |
| mypy | `.venv/bin/mypy tooling/ --config-file tooling/pyproject.toml` | Success: no issues found in 42 source files | 0 |

ruff config selects `E,F,W,I,B,UP,RUF` and ignores `E501`. There is no separate
formatter step (no `ruff format`/black in the documented flow); style is enforced
by lint plus the editorial style guide DOC-009.

## Validators

Command: `make -k validate PYTHON=.venv/bin/python`. All nine pass (exit 0).

| Validator | Result | Notes |
|---|---|---|
| frontmatter | OK | 160 markdown files validated |
| crossrefs | OK | framework_refs resolve across 160 files |
| signatures | OK | 0 approved policy/plan artefacts to check |
| supersession | OK | 160 revisions, chains consistent |
| law_references | OK (with warning) | `AT.NISG-2026: snapshot age 26d exceeds cadence 14d` |
| calendar | OK | 4 milestones, 0 overdue beyond 30d |
| bilingual | OK | 0 declared-bilingual artefacts |
| doc_type_coverage | OK | every schema doc_type has a template |
| registers | OK | assets/facilities/networks/suppliers/data/zones resolve |

The `law_references` stale-snapshot line is a non-fatal warning (the validator
still exits 0). It reflects operational currency, not a code defect, and is driven
by the snapshot date relative to the configured 14-day cadence.

## Other documented workflows (smoke)

| Workflow | Command | Result | Exit |
|---|---|---|---|
| currency-check | `make currency-check PYTHON=.venv/bin/python` | runs; reports 15 never-collected evidence tasks, 72/93 controls without an evidence task bound | 0 |
| instantiate (dry-run) | `instantiate.py --config instance/config.yaml --dry-run` | 163 files processed, no unresolved placeholders | 0 |
| pdf (html-only) | `render_pdf.py template/governance/policy/P-010-...md --html-only` | HTML written (10719 bytes) | 0 |
| audit pack | `build_audit_pack.py --audit stage-1` | pack built under `dist-audit-pack/` | 0 |

`make pdf`/`make soa-pdf` to actual PDF require WeasyPrint, which is absent here;
the renderer's HTML fallback path was exercised instead. The never-collected
evidence tasks and unbound controls are expected for a skeleton-state repository
(LIMITATIONS L1), not defects.

Note: `build_audit_pack.py` writes to `dist-audit-pack/`, which is not in
`.gitignore` (only `dist/` is). Recorded as S-002.

## CI drift assessment

CI (`ci.yml`) installs `tooling/[dev]` and runs ruff, mypy, `make test`, and
`make validate` on Python 3.14. Locally the same four steps pass on Python 3.11
with manually installed dependencies. The material drift is the interpreter
version: CI 3.14 vs the project's declared `>=3.12` vs this environment's 3.11.
`make bootstrap` is the only documented step that does not run here, for the
interpreter reason above. No other CI-vs-local behavioural drift was observed.

## Baseline summary

| Gate | Status |
|---|---|
| Build (`make bootstrap`) | FAIL on Python 3.11 (requires 3.12+); see Q-002 |
| Tests | 102 passed, 0 failed (0.71 s) |
| Coverage | 78 % |
| ruff | clean |
| mypy | clean |
| Validators | 9/9 pass (1 non-fatal currency warning) |

The repository is in good health: green tests, clean lint and types, passing
validators. The only true baseline gate failure is the documented bootstrap on
Python 3.11, which is an interpreter-version and documentation issue rather than a
code defect.
