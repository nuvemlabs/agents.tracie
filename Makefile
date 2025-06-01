.PHONY: install run test lint format clean docker-build docker-run help

# Variables
POETRY := poetry
PYTHON := $(POETRY) run python
PYTEST := $(POETRY) run pytest
BLACK := $(POETRY) run black
ISORT := $(POETRY) run isort
FLAKE8 := $(POETRY) run flake8
MYPY := $(POETRY) run mypy

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	$(POETRY) install --with dev

run: ## Run the agent interactively
	$(PYTHON) -m agent.core

run-cli: ## Run agent with query (usage: make run-cli q="your question")
	$(PYTHON) src/scripts/run_agent.py "$(q)"

test: ## Run tests
	$(PYTEST) -v

test-cov: ## Run tests with coverage
	$(PYTEST) -q --cov=agent --cov-report=term-missing

lint: ## Run all linting tools
	$(ISORT) --check-only .
	$(BLACK) --check .
	$(FLAKE8) src/
	$(MYPY) src/

format: ## Format code
	$(ISORT) .
	$(BLACK) .

pre-commit: ## Run pre-commit hooks
	$(POETRY) run pre-commit run --all-files

clean: ## Clean up cache and build files
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf dist/ build/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/

docker-build: ## Build Docker image
	docker build -t agents-tracie:latest .

docker-run: ## Run Docker container (requires .env file)
	docker run --env-file .env agents-tracie:latest

docker-interactive: ## Run Docker container interactively
	docker run -it --env-file .env agents-tracie:latest

# Example usage targets
example-basic: ## Run basic example
	$(PYTHON) src/scripts/run_agent.py "What is artificial intelligence?"

example-search: ## Run search example (requires SERPAPI_KEY)
	$(PYTHON) src/scripts/run_agent.py "What's the latest news about AI?"
