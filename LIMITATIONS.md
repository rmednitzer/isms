# Known limitations

> **Status**: draft
> **Last reviewed**: 2026-05-14

This document is the counterpart to the stated-purpose paragraph in
`README.md`. Where `README.md` describes what the repository is, this
document describes what it is not, and what work would be required to
change that.

Naming a limit is not the same as scheduling a fix. Some limits are
deliberate scope decisions that match the repository's identity as an ISMS
framework with one instance deployment, not as a general-purpose ISMS
platform. Naming them is part of the assurance posture.

## L1. Repository is at skeleton state; certification timeline drives content population

**Current state.** `README.md` declares the state as "Skeleton. Content
population proceeds per docs/certification-timeline.md." The two-layer
design (template/, instance/, framework-refs/, tooling/) is structurally
complete; substantive content under each is incomplete.

**Implication.** A reader expecting a fully populated ISMS framework will
find structure and tooling but limited content depth. The repository is a
base from which to populate, not a complete artefact set.

**What would close it.** Authoring per the certification timeline:
template policies and SOPs, fully populated framework references, the
worked example under `examples/instance-acme/`, and validation rules under
`tooling/validators/`.

**Intended scope.** Ongoing per certification timeline; not addressed in
this PR.

## L2. Template-vs-instance boundary is documented but tooling-enforced only on render

**Current state.** `docs/document-control.md` defines the boundary between
template content (framework, Apache-2.0) and instance content (deployment-
specific, confidential to the deploying organisation). `tooling/instantiate.py`
produces an instance from the template plus `instance/config.yaml`. CI does
not reject a PR that introduces deployment-specific content (real
organisation name, real risk register entries) into the template layer.

**Implication.** A contributor unfamiliar with the boundary could leak
instance content into template files. Discovery is review-time, not
CI-time.

**What would close it.**

- Tier 2: a CI sanitisation check that scans for organisation-specific
  markers (configurable denylist) in `template/`, `tooling/`,
  `framework-refs/`, `docs/`, `examples/`. Out of scope: scanning
  `instance/`, which is the right place for instance content.
- Tier 3: structured validation of the instantiation contract; CI that
  re-runs instantiation against a test config and diffs the result.

**Intended scope.** Tier 2 is a focused follow-up.

## L3. eIDAS QES signing depends on an external Qualified Certificate Authority

**Current state.** `docs/signature-policy.md` requires PAdES-signed PDFs
for governance artefacts (policies, Statement of Applicability, management
review minutes, audit statements, Selbstdeklaration). The repository
tooling under `tooling/signers/` integrates with external Qualified
Certificate Authority workflows; the QES itself is issued by an external
QTSP per eIDAS Regulation (EU) 910/2014 and the eIDAS 2 amendment.

**Implication.** The repository cannot produce a QES on its own; the
adopting organisation must establish a relationship with a Qualified Trust
Service Provider and follow the QTSP's signing workflow. Git-signed
commits attest integrity within the ISMS; they are not eIDAS signatures.

**What would close it.** Out of scope (external dependency).

**Intended scope.** No close-out planned. Limit named for honest framing.

## L4. NISG 2026 transposition state is fresh and likely to drift

**Current state.** NISG 2026 (Austria, BGBl. I Nr. 94/2025) enters into
force 2026-10-01. Implementing acts, supervisory authority procedures, and
the details of § 33 Selbstdeklaration are still being elaborated.
`framework-refs/sources/registry.yaml` tracks the law snapshots; the
rendered guidance is based on the law text as of the snapshot date.

**Implication.** Adopters must verify currency against the Bundesamt für
Cybersicherheit's published procedures and CERT.at's incident reporting
portal at the time of operational use, not at the snapshot date.

**What would close it.** Out of scope until the implementing acts and
supervisory procedures stabilise. The drift-watch concept (see L5) addresses
the currency-monitoring aspect.

**Intended scope.** Tier 1 framing in this PR.

## L5. Drift-watch on regulatory citations is partial

**Current state.** `make currency-check` checks snapshot ages and reference
coverage. Time-sensitive citations include NIS2 transposition status, AI
Act phased application milestones, NISG 2026 implementing acts, ISO
standard revisions, and harmonised standards publication state under the
CRA. The cadence per citation is not formalised in a registry that CI
enforces.

**Implication.** A reader cannot tell, in CI, whether a citation in the
registry is overdue against the cadence the citation type implies.

**What would close it.** A `framework-refs/sources/drift-watch.yaml`
registry listing time-sensitive citations with `last_reviewed` and
`cadence`; a CI check that flags overdue entries. Some of this exists
already in `make currency-check`; formalising the cadence per citation
is the gap.

**Intended scope.** Tier 2 (focused follow-up).

## L6. REUSE per-file SPDX retrofit not landed

**Current state.** REUSE 3.3 compliance is asserted at the repository level
via `REUSE.toml` and `LICENSES/Apache-2.0.txt`; CI verifies via
`.github/workflows/reuse.yml`. Existing files do not carry per-file SPDX
headers.

**Implication.** REUSE-compliant at aggregate level. Sufficient under
REUSE 3.3. Some tooling downstream of SBOM generators prefers per-file
headers; for those tools the aggregate assertion is consulted.

**What would close it.** Retrofit PR adding SPDX headers to every authored
file under template/, tooling/, docs/, framework-refs/. Instance files
are confidential and not in scope.

**Intended scope.** Tier 2 (deferred follow-up).

## L7. Multi-jurisdiction extension to ISO/IEC 27701:2025 and other regimes is structural only

**Current state.** README declares the framework as "Extensible to ISO/IEC
27701:2025 (privacy information management)" and notes "Multi-jurisdiction
sources tracked in framework-refs/sources/registry.yaml". The Austrian-
primary jurisdiction is exercised in `instance/config.yaml`. A second
jurisdiction (German BSI, French ANSSI, Italian ACN) is not exercised in
the committed examples.

**Implication.** The extension claim is structural (the design admits other
jurisdictions); operational evidence is single-jurisdiction. An adopting
organisation in a non-Austrian jurisdiction must extend the framework-refs
registry and validate that the tooling handles their specific authority
workflows.

**What would close it.** A second instance under `examples/` exercising a
different jurisdiction (or ISO 27701) would demonstrate extensibility.
Out of scope until the certification timeline reaches that milestone.

**Intended scope.** No close-out planned in this PR.

## How to read this document

- If you are using the repository as a framework for an ISO 27001 / NISG
  2026 ISMS in Austria: L1 (skeleton state) is the load-bearing limit;
  most of the content depth is ahead, not behind.
- If you are using the repository as a basis for a different jurisdiction:
  L7 applies; the structural extensibility is real but the operational
  evidence is single-jurisdiction.
- If you are using the repository as a substitute for accredited
  certification: it is not one. ISO 27001 certification is issued by an
  accredited certification body.

## Updating this document

Limits are reviewed under the same cadence as `STATUS.md` and
`CHANGELOG.md`. When a limit is closed, the entry is moved to a `Closed
limits` section.
