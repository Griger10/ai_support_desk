[group("lint-and-format")]
@backend-format:
    cd backend && VIRTUAL_ENV= uv run ruff format
    cd backend && VIRTUAL_ENV= uv run ruff check --fix
    cd backend && VIRTUAL_ENV= uv run mypy --no-incremental
