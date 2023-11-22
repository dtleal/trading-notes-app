.PHONY: all build start migrate makemigrations shell populate_database

all: build makemigrations migrate start

build: ## Build the Docker image
	@docker-compose build

makemigrations: ## Create any new migrations
	@docker-compose up directory -d
	@docker-compose run --rm directory /bin/bash -x -c 'python mysite/manage.py makemigrations'

migrate: ## Run any new migrations
	@docker-compose up directory -d
	@docker-compose run --rm directory /bin/bash -x -c 'python mysite/manage.py migrate'

db_populate: ## Run any new migrations
	@docker-compose up directory -d
	@docker-compose run --rm directory /bin/bash -x -c 'python mysite/manage.py populate_database'

start: ## Start the API in the background
	@docker-compose up directory -d

shell: start ## Get a Django shell
	@docker-compose exec directory python mysite/manage.py shell

bash:
	@docker-compose exec directory bash

runserver:
	python manage.py runserver

.PHONY: ruff
ruff:
	poetry run ruff . --fix

.PHONY: black
black:
	poetry run black .

.PHONY: autofmt
autofmt: ruff black

.PHONY: poetrycheck
poetrycheck:
	poetry check --lock

.PHONY: openapi-files
openapi-files:
	poetry run python ./openapi/combine_openapi.py
	# Used to parse public routes only into a swagger file.  Use for postman file given to customers.
	poetry run python ./openapi/parse_public_openapi.py
