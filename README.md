# FastAPI template

## Tools

- FastAPI
- SQLAlchemy Core 1.4
- Poetry
- Linters and formatters: mypy, black, isort, flake8
- Commands: Typer 
- pytest
- Docker
- Celery(WIP)
- Kafka(WIP)
- Sentry(WIP)

## Run project


```shell
docker-compose up app
```


### Run tests

```shell
docker-compose run --rm test
```


### Database migration

*   autogenerate migration

```shell
docker-compose run --rm alembic-autogenerate "Migration message"
```

*   upgrade to latest version

```shell
docker-compose run --rm alembic upgrade heads
```

*   upgrade to previous version

```shell
docker-compose run --rm alembic downgrade -1
```
