.PHONY: help	
help:
	@echo Usage:
	@echo "  make [target]"
	@echo
	@echo Targets:
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "  %-30s %s\n", $$1, $$NF \
		 }' $(MAKEFILE_LIST)

.PHONY: test 
test: ## run server locally sourcing tokens from .env
	@./scripts/test.sh

.PHONY: bd
build: ## build package dist 
	@./scripts/build.sh

.PHONY: publish
publish: ## publish dist to pypi
	@./scripts/publish.sh $(service)

.PHONY: dev
x86: ## build dev server docker image
	@./scripts/docker.sh

.PHONY: compose 
compose: ## build wellness bot for dev
	@./scripts/compose.sh
