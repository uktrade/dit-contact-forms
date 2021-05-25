.DEFAULT_GOAL := help

.EXPORT_ALL_VARIABLES:
DJANGO_SETTINGS_MODULE=config.settings.docker_development

##@ Help
help: ## Show this screen
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@echo ""

##@ Setup
build: template-files # builds the docker containers
	docker-compose pull
	docker-compose build
	docker-compose -f test.yml -p contact-forms-tests build

first-time-init: ## prepares system for first run
	@echo -e "\n\n\n\t\t===>> preparing system for first run, might take a while\n\n\n"
	@docker-compose run --rm contact_forms bash -c " \
		export DJANGO_SETTINGS_MODULE=config.settings.docker_development; \
		export DJANGO_BASE_DIR=$(pwd) ; \
		python manage.py collectstatic --noinput
	"

template-files: ## creates template files
	# ensure needed .env files are present
	@test -f .env \
		&& echo ".env file exists, not creating" \
		||  cp .env.template .env
	@test -f .env.test \
		&& echo ".env.test file exists, not creating" \
		||  cp .env.test.template .env.test

	@echo -e "\n\n\n\n\n\n \
		===>> Please edit .env and .env.test and update them with your credentials  \n\n \
	"
setup: first-time-init template-files ## first run setup
	@ echo "run "make help" for a list o availabe options"

##@ project
ssh: ## runs a bash shell on the main container
	docker-compose run --rm contact_forms bash

up: ## starts the containers
	docker-compose up -d

down: ## downs the containers
	docker-compose down

test: ## runs tests in a container
	docker-compose -f test.yml -p contact-forms-tests up --abort-on-container-exit --exit-code-from contact_forms

restart: down up ## alias for make down up

shell: ## runs a bash shell in the contact forms container
	docker-compose exec contact_forms /bin/bash
