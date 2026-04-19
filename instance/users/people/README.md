# People

One markdown file per person bound to roles in `instance/config.yaml` and `users/roles.yaml`.

## Format

```yaml
---
person_id: person:alice
legal_name: "Alice Example"
email: "alice@example.at"
roles: ["CISO", "ISMS-Manager"]
signing_keys:
  gpg: "1234567890ABCDEF1234567890ABCDEF12345678"
  ssh: "SHA256:abc123..."
qes_certificate_serial: "TODO after QES onboarding"
employment_start: "2025-01-15"
background_check_completed: true
training_completed:
  - isms_induction: "2025-01-20"
  - security_awareness_annual: "2025-11-10"
---
```

Commit per-person files here. This directory contains personal data; classify restricted.
