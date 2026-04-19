# Instance directory

This directory holds the concrete deployment of the ISMS template for one organisation.

## What goes here

- `config.yaml`: the single source of truth for this deployment. Every placeholder in `template/` resolves against this file.
- `users/`: role-to-person bindings; separation-of-duties matrix.
- `governance/`: rendered governance artefacts (produced by `python tooling/instantiate.py`).
- `operations/`: live operational records (incidents, changes, audits, exercises, reviews, access reviews).
- `evidence/`: append-only evidence tree with signed manifests and QES-signed PDFs.

## Initial instantiation

1. Edit `config.yaml` replacing every TODO marker with real values.
2. Populate `users/people/` with per-person records.
3. Run `python tooling/instantiate.py --config instance/config.yaml`.
4. Review the rendered governance artefacts under `governance/`.
5. Commit the rendered output alongside `config.yaml`.

## Re-rendering

Re-run `python tooling/instantiate.py` after any change to `config.yaml` or to `template/`. The renderer is idempotent and preserves files that have diverged from the template (manual edits are respected; rendering is additive for new files only, never destructive).

## Evidence structure

Evidence is laid out as:

```
evidence/
|-- YYYY/MM/DD/control-<ID>/     attestations + captured artefacts
|-- manifests/{daily,weekly,monthly}/   signed manifest chain
`-- signatures/                  QES-signed governance PDFs
```

## Privacy

This directory contains confidential and restricted content (real role-holder names, real asset identifiers, real evidence). Do NOT push to a public repository.
