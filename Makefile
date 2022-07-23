.DEFAULT_GOAL := help

help: ## Shows this help message
	@printf "\033[1m%s\033[36m %s\033[32m %s\033[0m \n\n" "Development environment for" "ludeeus/pytraccar" "";
	@awk 'BEGIN {FS = ":.*##";} /^[a-zA-Z_-]+:.*?##/ { printf " \033[36m make %-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST);
	@echo

requirements: install-poetry ## Install requirements
	@poetry install
	@poetry check

install: ## Install pytraccar
	@poetry install

install-poetry:
	@curl -sSL https://install.python-poetry.org | python3 -

build: ## Build the package
	@poetry build

test: ## Run all tests
	@poetry run pytest tests -rxf -x -v -l --cov=./ --cov-report=xml

lint: isort black mypy ## Lint all files

coverage: ## Check the coverage of the package
	@poetry run pytest tests -rxf -x -v -l --cov=./ --cov-report=xml > /dev/null
	@poetry run coverage report

isort:
	@poetry run isort pytraccar

isort-check:
	@poetry run isort pytraccar --check-only

black:
	@poetry run black --fast pytraccar

black-check:
	@poetry run black --check --fast pytraccar

mypy:
	@poetry run mypy --strict pytraccar