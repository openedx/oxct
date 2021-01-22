.DEFAULT_GOAL := help

###### Docker

docker-build: ## build the oxct Docker image
	docker-compose build

docker-run:  ## run a production-ready platform with docker-compose
	docker-compose up

###### Development & Testing

compile-requirements: ## compile requirements files
	pip-compile requirements/base.in
	pip-compile requirements/dev.in

upgrade-requirements: ## upgrade requirements files
	pip-compile --upgrade requirements/base.in
	pip-compile --upgrade requirements/dev.in

test: test-lint test-unit test-format  ## run unit tests

test-lint:  ## run linting tests
	pylint --errors-only oxct/ tests/

test-format:  ## run code formatting tests
	black --check --diff ./oxct

test-unit:  ## run unit tests
	python -m unittest

format:  ## format the code to comply with black rules
	black ./oxct

dev-redis: ## run a redis instance for development purposes
	docker-compose run --rm --publish=127.0.0.1:6379:6379 redis

dev-server: ## run a development server
	FLASK_APP=oxct/server/main.py FLASK_DEBUG=1 OXCT_REDIS_HOST=127.0.0.1 OXCT_LOG_LEVEL=DEBUG flask run

ESCAPE = 
help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/\n               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'
