# Tests

## Setup
```bash
# Using uv
uv pip install -e ".[dev]"

# Using pip
pip install -e ".[dev]"
```

## Run Tests
```bash
# Using uv
uv run pytest
uv run pytest --cov=scripts  # with coverage

# Using pip
pytest
pytest --cov=scripts  # with coverage
```