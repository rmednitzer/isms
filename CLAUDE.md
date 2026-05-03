# CLAUDE.md

Operating instructions for Claude Code sessions against this repository.

## Mandate

Assist with ISMS operation: drafting, validation, evidence collection, and audit packaging. Do not make governance decisions. Every commit requires explicit human authorisation.

This repository implements an Information Security Management System aligned with ISO/IEC 27001:2022, NISG 2026 (Austria), Implementing Regulation (EU) 2024/2690, and GDPR Art. 32. Authority-facing artefacts are German; internal artefacts default to English (per-instance via `instance/config.yaml`).

## Repository orientation

Two-layer design plus shared infrastructure. Read `docs/operating-contract.md` (DOC-003) before any non-trivial task.

| Path | Role | Editing posture |
|---|---|---|
| `template/` | reusable framework with `{{PLACEHOLDERS}}` | governed; revision-bumped |
| `instance/` | one concrete deployment | governed; revision-bumped |
| `instance/evidence/` | append-only attestations and signed PDFs | append-only; never modify history |
| `instance/users/` | role-to-person bindings | control-of-controls |
| `framework-refs/` | law snapshots, registry, calendar, deltas | authoritative; deltas only via SOP-101, SOP-102, SOP-103 |
| `docs/` | repo-level operating rules (DOC-001 through DOC-009) | governed |
| `tooling/` | schemas, validators, collectors, signers, packagers, renderer | tested; touched via PR with `make test` |
| `.github/` | CI, CODEOWNERS, dependabot | control-of-controls |
| `.gitsigners` | git signing key registry | control-of-controls |

The repo is standalone per DOC-004: no runtime dependency on external skill stacks, MCP servers, or cloud GRC platforms. `make validate` and `make pack` complete offline.

## Pre-flight checks

Before acting on any task, verify:

1. The current branch is not `main`. The `no-commit-to-branch` pre-commit hook blocks direct commits there; branch protection rejects direct pushes.
2. `git config commit.gpgsign` is true and a signing key is registered (GPG or SSH-sig). If not, stop and ask the human to configure it.
3. `.venv` exists, or `make bootstrap` has been run. The Makefile defaults `PYTHON` to `.venv/bin/python`; override with `PYTHON=python` only in CI contexts.
4. The task does not fall under "Workflows that require explicit human confirmation" without a fresh confirmation in the conversation.
5. GNU Make is available (the Makefile uses GNU pattern substitution and static pattern rules; BSD make will not work).

## Hard rules

1. **Signed commits required.** No commits without verified signing configuration. If `git config commit.gpgsign` or SSH signing is not set, stop and ask the human to configure it.
2. **Evidence is append-only.** No edits to existing files under `instance/evidence/` that change content or rewrite history. Corrections are additive (a new attestation with a `supersedes` field), never destructive. New evidence goes in new dated files.
3. **No fabrication.** Do not invent approvals, signatures, signed PDFs, or `signature_ref` paths. If a file claims `status: approved` but no matching record exists in `instance/evidence/signatures/`, flag and stop.
4. **No bypassing validators.** If `make validate` or `make test` fails, report and stop. Do not delete failing assertions, exclude files, weaken schemas, or suppress errors to "fix" the symptom. Fix the cause or hand back.
5. **Control-of-controls files require per-change authorisation.** No modifications to `.gitsigners`, `.github/workflows/`, `.github/CODEOWNERS`, `instance/users/roles.yaml`, or `instance/users/separation-of-duties.yaml` without explicit separate human authorisation per change.
6. **Incidents stay outside the merge pipeline.** Never draft or submit an incident report on behalf of the human. Incident response operates outside the merge pipeline. Prepare content for review; the human submits to CERT.at and the Bundesamt. NIS2 timing windows (24h Frühwarnung, 72h notification, 1 month final report) are operational, not PR-driven.
7. **No secrets, ever.** Do not commit API tokens, credentials, private keys, signing material, or real personal data of identified individuals. If encountered, stop, recommend redaction, and recommend rotation. The `detect-private-key` pre-commit hook is a backstop, not a substitute for discipline.
8. **No direct commits or pushes to `main`.** All changes flow via PR with CODEOWNER approval per DOC-005. Branch protection and the `no-commit-to-branch` hook enforce this; do not attempt to bypass either.

## Workflows you can drive

Concrete procedures Claude executes end to end. Running these is permitted; committing or pushing the resulting changes still requires explicit human authorisation per the Mandate, in addition to the signing-configuration check in Hard Rule 1.

### Instantiation

Read `instance/config.yaml`. Run `python tooling/instantiate.py --config instance/config.yaml`. Report unresolved placeholders. Re-rendering is idempotent; re-run whenever `config.yaml` changes or `template/` is updated.

### Drafting a new artefact

1. Identify `doc_type` (policy, procedure, standard, plan, record, report) and ID prefix per DOC-001 § 5 (table below).
2. Copy the front-matter template from `docs/document-control.md`.
3. Use the section skeleton from `docs/style-guide.md` § 7 matching the `doc_type`.
4. Set `status: draft`, `revision: 1`, `approved_date: null`, `approved_by: null`, `signature_ref: null`.
5. Open a branch named `<type>/<slug>` per DOC-005 § 3 (e.g. `policy/p-005-revision-2`).
6. Run `make validate` and iterate until clean.

### Revising an existing artefact

1. Open new revision `N+1` as `status: draft` with `supersedes_revision: N`.
2. The previous revision keeps its status until the new revision is approved; at approval the previous becomes `status: superseded`.
3. Editorial-only changes (typography, formatting) do not bump revision; record as an editorial commit referencing the original approval commit.
4. Update the revision-history table.

### Validation

`make validate` (parallelisable with `-j`). Validators in `tooling/validators/`:

- `validate_frontmatter.py` enforces control fields per DOC-001 § 3.
- `validate_crossrefs.py` checks `framework_refs` resolve against `template/governance/controls/`.
- `validate_signatures.py` checks `signature_ref` paths exist; signed-commit enforcement on main.
- `validate_supersession.py` checks revision chains are consistent.
- `validate_law_references.py`, `validate_calendar.py`, `validate_bilingual.py`, `validate_doc_type_coverage.py`, `validate_registers.py`.

If a validator fails, do not silence it. Report, propose root-cause fix, hand back.

### Currency check

`make currency-check` runs `evidence_age_report.py` and `control_coverage.py` against committed files only.

### Law snapshot fetch

`make snapshot-fetch` requires network. The fetcher writes new dated files under `framework-refs/snapshots/`; existing snapshot files are immutable and are never overwritten or edited (any apparent modification of an existing snapshot is a defect, stop). Diff against existing snapshots after fetch. If material changes are detected, propose an impact assessment under `framework-refs/impact-assessments/`; creating or closing one needs explicit human confirmation (see below).

### Audit pack

`make pack AUDIT=<stage-1|stage-2|surveillance-YYYY|selbstdeklaration>` once governance and evidence preconditions are met.

### PDF rendering

- `make pdf DOC=<path/to/file.md>` for a single artefact.
- `make soa-pdf` for the Statement of Applicability.
- WeasyPrint is required; the renderer regenerates a cover page from front-matter.

### Tests and lint

`make test` runs `tooling/tests` via pytest. Lint with `ruff check tooling/ --config tooling/pyproject.toml`. CI runs both on every PR.

## Workflows that require explicit human confirmation

Each item requires a fresh, in-conversation authorisation. Prior authorisation does not extend to subsequent operations.

- Committing any file with `status: approved`.
- Committing or modifying any file under `instance/evidence/signatures/`.
- Changing `framework-refs/sources/registry.yaml` (the law-source registry).
- Changing any schema under `tooling/schemas/`.
- Creating or closing an impact assessment under `framework-refs/impact-assessments/`.
- Editing files under `framework-refs/snapshots/` (these are immutable law snapshots; new fetches go in new dated files).
- Setting `interim_signature: true` outside the 90-day onboarding window per DOC-002 § 5.
- Any change to `.gitsigners`, `.github/CODEOWNERS`, `.github/workflows/`, role definitions in `instance/users/roles.yaml`, or `instance/users/separation-of-duties.yaml`.

## Document ID conventions

Per DOC-001 § 5:

| Prefix | Type | Example |
|---|---|---|
| DOC- | repo-level control documents | DOC-001 |
| P- | policy | P-005 |
| SOP- | procedure | SOP-001 |
| STD- | standard | STD-001 |
| PLAN- | plan | PLAN-001 |
| REC-YYYY- | record | REC-2026-001 |
| INC-YYYY- | incident record | INC-2026-001 |
| RFC- | change request | RFC-0001 |
| IA-YYYY- | impact assessment | IA-2026-001 |
| DEC-YYYY- | architectural decision record | DEC-2026-001 |
| TMPL- | operational template | TMPL-001 |

Status lifecycle: `draft` to `under_review` to `approved` to `superseded` (or `retired`). Transitions per DOC-001 § 6. Approval of policies and plans additionally requires QES per DOC-002 (or `interim_signature: true` during the interim window).

## Branching and PRs

Per DOC-005:

- Branches named `<type>/<slug>`, e.g. `policy/p-005-revision-2`, `tooling/validator-frontmatter-fix`, `law/nisg-2026-verordnung-1-impact`.
- Material and structural changes require an RFC under `instance/operations/changes/rfcs/RFC-NNNN.md`. PR references the RFC.
- PRs carry signed commits, pass `make validate` and `make test`, and require CODEOWNER approval per the paths touched.
- Status transitions to `approved` carry the QES-signed PDF (or `interim_signature: true` per DOC-002 § 5).
- Reverts are not editorial; they require the same CODEOWNER approval as the original change.

## Register

Governance artefacts (policies, SOPs, standards) are read by auditors, legal reviewers, and the Leitungsorgan. Register is formal and precise.

- Imperative mood for procedure steps. Declarative mood for policy statements.
- Active voice unless the actor is deliberately unspecified by policy.
- ISO/IEC Directives Part 2 verbs: `shall`, `should`, `may`, `shall not`. No marketing language. No hedging.

Peer-engineering informality belongs in commit messages and internal notes, not in policy text.

## Language

- Internal artefacts: English by default. Per-instance override via `instance/config.yaml` `entity.primary_language`.
- Authority-facing artefacts (Selbstdeklaration per NISG 2026 § 33, CERT.at Frühwarnung, Bundesamt correspondence, registration records): German is authoritative.
- When a document declares `bilingual: true`, both `<doc_id>.<lang>.md` versions live side by side and `validate_bilingual.py` enforces structural parity.
- Code, comments, commit messages, PR descriptions: English.
- Legal citations in original language: German for Austrian federal law (§, Abs., Z.); English for EU law (Art., para.). Translations are explicit paraphrases, not authoritative.
- Commit messages: English, imperative mood, short.

## Formatting

DOC-009 (`docs/style-guide.md`) is authoritative. Quick reference:

- UTF-8, Unix line endings, soft-wrap at 100 where practical.
- No em dashes, no double dashes. Use comma, semicolon, period, parenthesis.
- Dates `YYYY-MM-DD`. Times 24h, prefer UTC `Z`. SI units with non-breaking space. Currency in EUR where user-facing.
- ATX headings, numbered top-level sections, GFM tables.
- Code blocks fenced with language hint (`shell`, `yaml`, `json`, `python`).
- Markdown front-matter per DOC-001 § 3.

## Standalone constraint

Per DOC-004:

- Validators, core collectors, packagers, and the renderer run against committed files only. No network calls.
- Network operations are confined to `tooling/collectors/optional/` and invoked via explicit targets (`make snapshot-fetch`, scheduled `currency-check.yaml`).
- The optional `isms-mcp` overlay (DEC-2026-008) is read-only, lives outside this repository, and is never imported by, required by, or invoked from `tooling/`, `Makefile`, or `.github/workflows/`.
- An auditor's clone plus `make bootstrap` reproduces all evidence without external dependency. Treat that property as the contract.

If a task seems to require an external dependency not already present, flag and propose a standalone alternative.

## Common mistakes to avoid

- Editing the in-body visible header to depart from front-matter. Front-matter is canonical; the renderer regenerates the cover page from it (DOC-001 § 4).
- Bumping revision for editorial changes (typography, formatting). Editorial-only goes as a commit referencing the original approval commit (DOC-001 § 6).
- Breaking supersession chains. `supersedes_revision` is required on every revision greater than 1; orphans fail `validate_supersession.py`.
- Marking a previous revision `status: superseded` before its successor is approved.
- Introducing em dashes or double dashes from generated text. Validators do not catch typography; reviewers do.
- Auto-linking cross-references in markdown. Use document IDs (`P-000`, `SOP-001`) in prose; reviewers verify.
- Assuming `make` is BSD make. The Makefile is GNU-only.
- Running validators as `python tooling/validators/...` on a fresh clone without `.venv`. Suggest `make bootstrap` first, or pass `PYTHON=python`.
- Committing `.venv/`, build artefacts, or `__pycache__/`. `.gitignore` covers these but verify before staging.
- Confusing git-signed commits with eIDAS QES. Git signing evidences authorship and integrity; QES (PAdES on PDF) evidences legal approval per DOC-002.

## When in doubt

Ask. One clarifying question is cheaper than an unauthorised commit. Cite the specific clause or document being relied on (for example, "Per DOC-001 § 6, may I bump the revision?").
