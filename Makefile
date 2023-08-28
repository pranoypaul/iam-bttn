.DEFAULT_GOAL:=help

.EXPORT_ALL_VARIABLES:

ifndef VERBOSE
.SILENT:
endif

# set default shell
SHELL=/usr/bin/env bash -o pipefail -o errexit

TAG ?= $(shell cat TAG)
POETRY_HOME ?= ${HOME}/.local/share/pypoetry
POETRY_BINARY ?= ${POETRY_HOME}/venv/bin/poetry
POETRY_VERSION ?= 1.3.2

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: show-version
show-version:  ## Display version
	echo -n "${TAG}"

.PHONY: build
build: ## Build iam package
	echo "[build] Build iam package."
	${POETRY_BINARY} build

.PHONY: install
install:  ## Install iam with poetry
	@build/install.sh

.PHONY: image
image:  ## Build iam image
	@build/image.sh

.PHONY: metrics
metrics: install ## Run iam metrics checks
	echo "[metrics] Run iam PEP 8 checks."
	${POETRY_BINARY} run flake8 --select=E,W,I --max-line-length 80 --import-order-style pep8 --statistics --count iam
	echo "[metrics] Run iam PEP 257 checks."
	${POETRY_BINARY} run flake8 --select=D --ignore D301 --statistics --count iam
	echo "[metrics] Run iam pyflakes checks."
	${POETRY_BINARY} run flake8 --select=F --statistics --count iam
	echo "[metrics] Run iam code complexity checks."
	${POETRY_BINARY} run flake8 --select=C901 --statistics --count iam
	echo "[metrics] Run iam open TODO checks."
	${POETRY_BINARY} run flake8 --select=T --statistics --count iam tests
	echo "[metrics] Run iam black checks."
	${POETRY_BINARY} run black -l 80 --check iam

.PHONY: unit-test
unit-test: install ## Run iam unit tests
	echo "[unit-test] Run iam unit tests."
	${POETRY_BINARY} run pytest tests/unit

.PHONY: integration-test
integration-test: install ## Run iam integration tests
	echo "[unit-test] Run iam integration tests."
	${POETRY_BINARY} run pytest tests/integration

.PHONY: coverage
coverage: install  ## Run iam tests coverage
	echo "[coverage] Run iam tests coverage."
	${POETRY_BINARY} run pytest --cov=iam --cov-fail-under=90 --cov-report=xml --cov-report=term-missing tests

.PHONY: test
test: unit-test integration-test  ## Run iam tests

.PHONY: docs
docs: install ## Build iam documentation
	echo "[docs] Build iam documentation."
	${POETRY_BINARY} run sphinx-build docs site

.PHONY: dev-env
dev-env: image ## Start a local Kubernetes cluster using minikube and deploy application
	@build/dev-env.sh

.PHONY: clean
clean: ## Remove .cache directory and cached minikube
	minikube delete && rm -rf ~/.cache ~/.minikube
