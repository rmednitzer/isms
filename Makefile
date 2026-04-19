.PHONY: help bootstrap instantiate validate currency-check snapshot-fetch pack selbstdeklaration test clean

PYTHON ?= .venv/bin/python
VENV ?= .venv
AUDIT ?=

help:
	@echo "isms Makefile targets:"
	@echo ""
	@echo "  bootstrap          create .venv and install tooling"
	@echo "  instantiate        render template/ into instance/ per instance/config.yaml"
	@echo "  validate           run all offline validators (no network)"
	@echo "  currency-check     check snapshot ages and reference coverage"
	@echo "  snapshot-fetch     refresh law snapshots from RIS and EUR-Lex (network required)"
	@echo "  pack AUDIT=<stg>   build audit bundle (stage-1 | stage-2 | surveillance-YYYY | selbstdeklaration)"
	@echo "  selbstdeklaration  build NISG 2026 § 33 self-declaration package"
	@echo "  test               run tooling unit tests"
	@echo "  clean              remove generated artefacts (not source)"

bootstrap:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e tooling/
	@test -x $(VENV)/bin/pre-commit && $(VENV)/bin/pre-commit install || true
	@echo "bootstrap complete. activate with: source $(VENV)/bin/activate"

instantiate:
	$(PYTHON) tooling/instantiate.py --config instance/config.yaml

validate:
	$(PYTHON) tooling/validators/validate_frontmatter.py
	$(PYTHON) tooling/validators/validate_crossrefs.py
	$(PYTHON) tooling/validators/validate_signatures.py
	$(PYTHON) tooling/validators/validate_supersession.py
	$(PYTHON) tooling/validators/validate_law_references.py
	$(PYTHON) tooling/validators/validate_calendar.py
	$(PYTHON) tooling/validators/validate_bilingual.py

currency-check:
	$(PYTHON) tooling/collectors/core/evidence_age_report.py
	$(PYTHON) tooling/collectors/core/control_coverage.py

snapshot-fetch:
	$(PYTHON) tooling/collectors/optional/fetch_ris.py
	$(PYTHON) tooling/collectors/optional/fetch_eurlex.py
	$(PYTHON) tooling/collectors/optional/detect_delta.py

pack:
	@if [ -z "$(AUDIT)" ]; then \
		echo "AUDIT=<stage-1|stage-2|surveillance-YYYY|selbstdeklaration> required"; \
		exit 2; \
	fi
	$(PYTHON) tooling/packagers/build_audit_pack.py --audit $(AUDIT)

selbstdeklaration:
	$(PYTHON) tooling/packagers/build_selbstdeklaration.py

test:
	$(PYTHON) -m pytest tooling/tests -v

clean:
	rm -rf dist/ build/ *.egg-info/ tooling/*.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
