sources = app tests

.PHONY: .uv
.uv:
	@uv -V || echo 'Install uv: https://docs.astral.sh/uv/getting-started/installation/'

.PHONY: install
install: .uv
	uv sync --frozen --all-extras

.PHONY: format
format: .uv
	uv run ruff check --fix $(sources)
	uv run ruff format $(sources)

.PHONY: lint
lint: .uv
	uv run ruff check $(sources)
	uv run ruff format --check $(sources)

.PHONY: test
test: .uv
	uv run pytest tests

.PHONY: run
run: .uv
	uv run litestar run