# Template placeholders

Inventory of placeholders used across `template/`. All must resolve during `python tooling/instantiate.py --config instance/config.yaml`; unresolved placeholders are fatal in `--strict` mode and a warning otherwise.

## Placeholder syntax

- `{{key.path}}` resolves against `instance/config.yaml`; nested paths supported.
- `{{#if key.path}}...{{else}}...{{/if}}` conditional block; truthiness determined by non-null, non-empty value.

## Placeholders in use

### Entity

| Placeholder | Type | Description |
|---|---|---|
| `{{entity.legal_name}}` | string | Full legal name including legal form |
| `{{entity.short_name}}` | string | Short name used in running prose |
| `{{entity.jurisdiction}}` | enum | at, de, ch, li, eu |
| `{{entity.legal_form}}` | string | e.g. GmbH, AG, OeG, KG, Verein, GmbH & Co KG |
| `{{entity.register_number}}` | string | Firmenbuchnummer or equivalent |
| `{{entity.address.street}}` | string | Street and number |
| `{{entity.address.postal_code}}` | string | Postal code |
| `{{entity.address.city}}` | string | City |
| `{{entity.address.country}}` | string | ISO 3166-1 name |
| `{{entity.primary_language}}` | enum | en or de |
| `{{entity.authority_language}}` | enum | en or de (authoritative for authority-facing) |
| `{{entity.draft_date}}` | date | Date of template instantiation, YYYY-MM-DD |

### Classification

| Placeholder | Type | Description |
|---|---|---|
| `{{classification.nisg2026_category}}` | string | wesentliche-einrichtung, wichtige-einrichtung, out-of-scope |
| `{{classification.nisg2026_sectors}}` | string | NISG 2026 Annex I sectors applicable |
| `{{classification.nisg2026_registration_id}}` | string | Bundesamt-issued ID (populated after registration) |
| `{{classification.gdpr_role}}` | string | controller, processor, joint-controller |
| `{{classification.iso27001_target_cert_date}}` | date | YYYY-MM-DD target for stage 2 certification |

### Scope

| Placeholder | Type | Description |
|---|---|---|
| `{{scope.statement_summary}}` | string | One-paragraph scope statement |
| `{{scope.included_locations}}` | string | Locations in scope |
| `{{scope.included_business_units}}` | string | Business units or services in scope |
| `{{scope.excluded_items}}` | string | Explicit exclusions |

### Feature flags

| Placeholder | Type | Description |
|---|---|---|
| `{{feature_flags.use_qes}}` | bool | QES signing active |
| `{{feature_flags.use_cyber_trust_austria}}` | bool | Cyber Trust Austria Platinum pursued |
| `{{feature_flags.bilingual_enforcement}}` | bool | Bilingual parity required for in-scope artefacts |
| `{{feature_flags.multi_entity}}` | bool | Multi-entity ISMS |

### Providers

Provider placeholders under `providers.*` are referenced by specific artefacts as they need them. See `instance/config.yaml` for the full catalogue.
