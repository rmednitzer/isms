# Examples

Worked examples that illustrate how the ISMS template is configured and
populated. Nothing in this directory is part of any real deployment; every
artefact uses fictitious entities, addresses, suppliers, and risk values.

The validators do not scan `examples/`. Files here will not affect
`make validate` or `make test`. Files here are also never instantiated into
`instance/` by `tooling/instantiate.py`.

## What each example shows

| Path | Shows |
|---|---|
| `instance-acme/` | A fully populated `instance/config.yaml`, a small set of populated registers, and a draft policy |

## How to use these

Read them. Do not copy `examples/instance-acme/config.yaml` over the real
`instance/config.yaml`; it is for orientation, not for running.

If you need to test the template end-to-end, use the example as a reference and
fill in real values in `instance/config.yaml` for your deployment.

## Conventions

- Every artefact uses `status: draft`. No example carries `status: approved`,
  because no QES-signed PDF exists for it.
- All entities, IDs, and personal data are fabricated.
- Dates are illustrative and do not necessarily reflect realistic timelines.
