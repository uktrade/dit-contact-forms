.DEFAULT_GOAL := help

COMPOSE_FILE ?= development.yml
.EXPORT_ALL_VARIABLES:
DJANGO_SETTINGS_MODULE=config.settings.docker_development

##@ Help
help: ## Show this screen
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@echo ""

##@ Setup
build: # builds the docker containers
	docker-compose  -f $(COMPOSE_FILE) pull
	docker-compose  -f $(COMPOSE_FILE) build

npm-install: ## install dependencies managed by npmand build gov.uk fronted framework
	docker-compose  -f $(COMPOSE_FILE) run --rm contact_forms sh -c " \
		npm install && \
		npm rebuild node-sass \
	"

npm-run-build: ## builds javascript dependencies
	docker-compose  -f $(COMPOSE_FILE) run --rm contact_forms npm run build

first-time-init: ## prepares system for first run
	@echo -e "\n\n\n\t\t===>> preparing system for first run, might take a while\n\n\n"
	@docker-compose  -f $(COMPOSE_FILE) run --rm contact_forms bash -c " \
		export DJANGO_SETTINGS_MODULE=config.settings.docker_development; \
		export DJANGO_BASE_DIR=$(pwd) ; \
		python manage.py collectstatic --noinput && \
		python manage.py migrate && \
		 python manage.py loaddata countries_data \
	"

template-files: ## creates template files
	# ensure needed .env files are present
	@test -f .envs/.development/.django \
		&& echo ".envs/.development/.django env file exists, not creating" \
		||  cp .envs/.development/.django.template .envs/.development/.django
	@test -f .envs/.test/.django \
		&& echo ".envs/.test/.django env file exists, not creating" \
		||  cp .envs/.test/.django.template .envs/.test/.django


	@test -f .envs/.development/.postgres \
		&& echo ".envs/.development/.postgres env file exists, not creating" \
		||  cp .envs/.development/.postgres.template .envs/.development/.postgres
	@test -f .envs/.test/.postgres \
		&& echo ".envs/.test/.postgres env file exists, not creating" \
		||  cp .envs/.test/.postgres.template .envs/.test/.postgres

	@echo -e "\n\n\n\n\n\n \
		===>> Please edit .envs/*/.django and .envs/*/.postgres and update them with your credentials  \n\n \
	"
setup: npm-install npm-run-build first-time-init template-files ## first run setup
	@ echo "run "make help" for a list o availabe options"

##@ project
ssh: ## runs a bash shell on the main container
	docker-compose -f $(COMPOSE_FILE) run --rm contact_forms bash

up: ## starts the containers
	docker-compose -f $(COMPOSE_FILE) up

down: ## downs the containers
	docker-compose -f $(COMPOSE_FILE) down

restart: down up ## alias for make down up

