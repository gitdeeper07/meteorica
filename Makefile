.PHONY: help install install-dev test lint format clean build docs serve

help:
	@echo "Available commands:"
	@echo "  make install      Install package"
	@echo "  make install-dev  Install with dev dependencies"
	@echo "  make test        Run tests"
	@echo "  make lint        Run linters"
	@echo "  make format      Format code"
	@echo "  make clean       Clean build artifacts"
	@echo "  make build       Build package"
	@echo "  make docs        Build documentation"
	@echo "  make serve       Serve documentation locally"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=meteorica

lint:
	ruff check meteorica/
	black --check meteorica/ tests/
	isort --check-only meteorica/ tests/
	mypy meteorica/

format:
	ruff check meteorica/ --fix
	black meteorica/ tests/
	isort meteorica/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf coverage.xml
	rm -rf htmlcov/
	rm -rf site/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

build: clean
	python -m build

docs:
	mkdocs build

serve:
	mkdocs serve

# Reports
reports-daily:
	@./scripts/generate_daily_reports.sh
