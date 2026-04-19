# framework-refs

Authoritative source registry, law snapshots, regulatory calendar, and crosswalk material.

## Structure

```
framework-refs/
|-- sources/registry.yaml            authoritative source list
|-- snapshots/                       per-source, per-version local copies
|   |-- at/
|   |-- eu/
|   `-- international/
|-- changelog/                       narrative change history per source
|-- currency/
|   |-- deltas/                      DLT-YYYY-NNN records from detect_delta
|   `-- history/                     archived prior snapshots
|-- calendar/regulatory-calendar.yaml  upcoming milestones
`-- impact-assessments/              IA-YYYY-NNN impact assessments for material deltas
```

## Populating snapshots

1. Run `make snapshot-fetch` (requires network; fetches from RIS and EUR-Lex).
2. Each source writes `<version>.<fmt>` files plus `<version>.meta.yaml` under the source's directory.
3. Fetched snapshots are automatically signed by the CI workflow if signing keys are present.

## Copyright handling

See `NOTICE.md` in this directory. Public law texts are reproduced under their respective regimes. Copyrighted standards (ISO/IEC) carry identifiers and titles only; full text must be obtained via a licensed copy.
