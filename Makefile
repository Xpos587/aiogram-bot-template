project_dir := .
bot_dir := bot

lang_dir := lang

# Lint code
.PHONY: lint
lint:
	@poetry run black --check --diff $(project_dir)
	@poetry run ruff $(project_dir)
	@poetry run mypy $(project_dir) --strict

# Reformat code
.PHONY: reformat
reformat:
	@poetry run black $(project_dir)
	@poetry run ruff $(project_dir) --fix

# Update translations
.PHONY: i18n
i18n:
	poetry run i18n multiple-extract \
		--input-paths $(bot_dir) \
		--output-dir $(lang_dir) \
		-k i18n -k L --locales $(locale) \
		--create-missing-dirs

# Make database migration
.PHONY: migration
migration:
	@poetry run alembic revision \
		--autogenerate \
		--rev-id $(shell python migrations/_get_next_revision_id.py) \
		--message "$(message)"

.PHONY: migrate
migrate:
	@poetry run alembic upgrade head

.PHONY: rollback
rollback:
	@poetry run alembic downgrade -1

.PHONY: run
run:
	@poetry run python -m bot || true
