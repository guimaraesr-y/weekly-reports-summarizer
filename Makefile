.PHONY: install install-dev format lint test coverage clean help

# Variables
PYTHON = python
VENV = .venv
SRC = src
TESTS = tests

# Colors for output
BLUE = \033[34m
GREEN = \033[32m
RED = \033[31m
RESET = \033[0m

help: ## Shows this help message
	@echo "$(BLUE)Available commands:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'

install: ## Installs production dependencies
	@echo "$(BLUE)Installing production dependencies...$(RESET)"
	$(PYTHON) -m pip install -r requirements.txt

install-dev: ## Installs development dependencies
	@echo "$(BLUE)Installing development dependencies...$(RESET)"
	$(PYTHON) -m pip install -r requirements-dev.txt

format: ## Formats code using autopep8 (according to PEP 8)
	@echo "$(BLUE)Formatting code with autopep8...$(RESET)"
	autopep8 --in-place --aggressive --aggressive --recursive $(SRC) $(TESTS)

lint: ## Runs flake8 linter
	@echo "$(BLUE)Checking code style...$(RESET)"
	flake8 $(SRC) $(TESTS)

test: ## Runs tests
	@echo "$(BLUE)Running tests...$(RESET)"
	pytest $(TESTS)

coverage: ## Generates test coverage report
	@echo "$(BLUE)Generating coverage report...$(RESET)"
	pytest --cov=$(SRC) --cov-report=term-missing $(TESTS)

coverage-html: ## Generates HTML coverage report
	@echo "$(BLUE)Generating HTML coverage report...$(RESET)"
	pytest --cov=$(SRC) --cov-report=html $(TESTS)
	@echo "$(GREEN)Report generated at htmlcov/index.html$(RESET)"

check: format lint test ## Runs all checks (format, lint, test)

clean: ## Removes temporary files and caches
	@echo "$(BLUE)Cleaning temporary files...$(RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +

venv: ## Creates a virtual environment
	@echo "$(BLUE)Creating virtual environment...$(RESET)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)Virtual environment created at $(VENV)$(RESET)"
	@echo "$(BLUE)Activate virtual environment with: source $(VENV)/Scripts/activate (Windows) or source $(VENV)/bin/activate (Unix)$(RESET)"
