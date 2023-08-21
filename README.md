# FastAPI template


## Project architecture
The app consists of several domains(like users, items, etc.)
Each domain has 3 layers of abstraction:

1. Handlers layer. Responsible for creating API route function, validation input user data, and creating/closing database connection at the start/end of each request. 
2. Service layer. It's a place for all business logic and additional validation. 
3. Database layer. Responsible for creating actual SQL queries and executing them.


## Tools

- FastAPI
- SQLAlchemy 2.0
- Poetry
- Linters and formatters: black, isort, ruff
- Commands: Typer 
- pytest
- Docker
- Celery and Redis
- Sentry
- Kafka(WIP)

## Before first commit
```shell
poetry install --only=dev
pre-commit install
```

## Environment variables
Environment variables for development can be found in .env.example. You must create app/.env file and fill missing
variables with value SET_VALUE from stage environment.


## Run application

- Using docker compose or prepared commands from makefile
```shell
docker compose up app
```
```shell
make dc-up
```
- Using local shell
    
1. Create virtual environment
```shell
poetry shell
```
2. Install all dependencies
```shell
poetry install --no-root
```
3. Start application
```shell
docker/start.sh
```

## Run worker
- Using docker compose
```shell
docker compose up worker
```
## Tests

- Using docker compose with any pytest flag or prepared makefile
```shell
docker compose run --rm test -s
```
```shell
make dc-test
```
```shell
make dc-test tests/integration
```
```shell
make dc-test-parallel
```
```shell
make dc-test-unit tests/unit
```
```shell
# run test and restart if code base is changed 
make dc-test-watch 
```
- All test running using pytest
- Option `--reuse-db` allow to use the same database without deleting it
- Parallel tests allow to run tests in parallel procceses. For each proccess created it's own database based on worker_id
- Option `--without-db` allow to run withou creating database and only for unit tests

## Database migration

- autogenerate migration

```shell
docker compose run --rm migrations alembic revision --autogenerate -m 'Migration message'
```
```shell
make dc-migrations 'Migration message'
```

- upgrade to latest version

```shell
docker compose run --rm migrations upgrade heads
```
```shell
make dc-migrate
```

- upgrade to previous version

```shell
docker compose run --rm alembic downgrade -1
```
```shell
make dc-migrate-rollback
```


## Run linters
- Run only check

```shell
make lint-check
```
    
- Run linters and modify files

```shell
make lint
```
