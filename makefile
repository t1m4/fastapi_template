#!make
.DEFAULT_GOAL := dc-test

# Makefile target args
args = $(filter-out $@,$(MAKECMDGOALS))


# Docker commands
dc-up:
	docker compose up -d app

dc-build:
	docker compose build --no-cache app

dc-down:
	docker compose down

dc-migrate:
	docker compose run --rm migrations alembic upgrade head

dc-migrate-rollback:
	docker compose run --rm migrations alembic downgrade -1

dc-history:
	docker compose run --rm migrations alembic history

dc-migrations:
	docker compose run --rm migrations alembic revision --autogenerate -m "$(MESSAGE)"

dc-logs:
	docker compose logs -f $(args)

dc-test-exec:
	docker compose run --rm test /bin/bash

dc-test:
	docker compose run --rm test pytest --reuse-db -svvl $(args)

dc-test-new-db:
	docker compose run --rm test pytest -svvl $(args)

dc-test-parallel:
	docker compose run --rm test pytest --reuse-db -svvl -n 2 $(args)

dc-test-unit:
	docker compose run --rm test pytest --without-db -svvl $(args)

dc-test-watch:
	docker compose run --rm test pytest --reuse-db -svvl -f --ff $(args)

dc-test-cov:
	docker compose run --rm test ./docker/test-ci.sh $(args)

dc-purge_celery: dc-up-app
	docker compose exec app celery -A scec purge

dc-app-exec: dc-up-app
	docker compose exec app $(args)

lint-check:
	black --check $(args)
	isort --check-only $(args)
	ruff check $(args)

lint:
	black $(args)
	isort $(args)
	ruff check --fix $(args)

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf dist *.egg-info
	rm -rf .cache
	rm -rf .pytest_cache
	rm -f coverage
	rm -f coverage.*
	rm -rf artifacts/*
