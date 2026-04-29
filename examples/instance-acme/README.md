# Example instance: Acme Widgets GmbH

Worked example of how a populated deployment looks. Every value is fictitious
and intentionally simple. Read this directory to understand the shape of a
real deployment before populating `instance/`.

## Contents

| File | Purpose | Conforms to |
|---|---|---|
| `config.yaml` | Fully populated `instance/config.yaml` | `tooling/schemas/config.schema.json` |
| `asset-register.yaml` | Three assets across information / software / service | `tooling/schemas/asset-register.schema.json` |
| `facilities.yaml` | Two facilities, four zones | `tooling/schemas/facilities-register.schema.json` |
| `networks.yaml` | Two segments with peering | `tooling/schemas/network-register.schema.json` |
| `supplier-register.yaml` | Hosting provider plus QTSP | `tooling/schemas/supplier-register.schema.json` |
| `data-inventory.yaml` | One processing activity (GDPR Art. 30) | `tooling/schemas/data-inventory.schema.json` |
| `risk-register.yaml` | Three risks with cross-references to assets and controls | `tooling/schemas/risk-register.schema.json` |
| `sample-policy-P-001-acceptable-use.md` | A drafted acceptable use policy showing populated front-matter and structure | `tooling/schemas/frontmatter.schema.json` |

## Walkthrough

The example illustrates a small Austrian manufacturer (Acme Widgets GmbH)
classified as a `wichtige-einrichtung` under NISG 2026, targeting ISO 27001
certification, and using A-Trust as its qualified trust service provider.

### Step 1: Read `config.yaml`

`config.yaml` is the single source of truth for an instance. Every
`{{placeholder}}` in `template/` resolves against keys here. Compare it with
the unfilled `instance/config.yaml` at the repo root to see what each field
expects.

Cross-references between this file and downstream registers:

- `entity.short_name` (Acme) appears in rendered policy bodies
- `roles.ciso.person_id` must match an entry under `instance/users/people/`
- `providers.qts_provider.name` (a-trust) gates SOP-201 ceremony procedure
- `feature_flags.bilingual_enforcement: true` activates `validate_bilingual.py`

### Step 2: Read the registers

The registers form a small graph:

```
facilities (FAC-001)
   |
   +-- zones (ZONE-003)
              |
              +-- assets (ASSET-0001) ---- data-inventory (DATA-001)
                              |                       |
                              +-- networks (NET-001)  +-- recipients --> suppliers (SUP-001)
                              |
                              +-- suppliers (SUP-001, SUP-002)
                              |
                              +-- depended on by ASSET-0002, ASSET-0003
```

The repo's `validate_registers.py` enforces that every reference in this
graph resolves. Try breaking a reference (e.g., set `ASSET-0001.location_ref:
FAC-999`) and run the validator from a copy to see the error.

### Step 3: Read the risk register

`risk-register.yaml` shows three risks at different lifecycle states
(`treating`, `treated`, `assessed`), each tied to assets and controls. Risks
reference controls by framework prefix (e.g., `iso27002:A.8.28`), the same
syntax used in policy `framework_refs`.

### Step 4: Read the sample policy

`sample-policy-P-001-acceptable-use.md` shows what a drafted policy looks
like once the placeholders are resolved and the body is filled. Compare with
`template/governance/policy/P-001-acceptable-use-policy.md` (which has
TODO-marked placeholders) to see the difference.

The policy is `status: draft`. It deliberately does not carry `status:
approved` because no QES-signed PDF exists for it. The repo's
`validate_signatures.py` rule requires every approved policy to point at a
real signature artefact under `instance/evidence/signatures/`.

## What this example does not include

- No incident records (`status` for incidents is operational, not
  illustrative)
- No evidence files (evidence is append-only and instance-specific)
- No signed PDFs (a real QTSP signature would need to be produced through
  the SOP-201 ceremony)
- No `instance/users/people/` entries (those would carry real personal data)

## How not to use this example

Do not:

- copy `config.yaml` over `instance/config.yaml` and run `make instantiate`
  expecting it to work, the real `instance/users/people/` directory will not
  contain the referenced person IDs
- treat any value here as advisory for a real organisation; the risk
  ratings, controls, and retention periods are illustrative only
