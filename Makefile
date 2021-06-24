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

.PHONY: build 
build: ## build package dist 
	@./scripts/build.sh

.PHONY: publish
publish: ## publish dist to pypi
	@./scripts/publish.sh $(service)

.PHONY: x86 
x86: ## build x86 server docker image
	@./scripts/docker.sh

.PHONY: compose 
compose: ## build wellness bot for x86
	@./scripts/compose.sh
