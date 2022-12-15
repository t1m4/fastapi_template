# FastAPI template


## Project architecture
The app consists of several domains(like users, items, etc.)
Each domain has 3 layers of abstraction:

1. Handlers layer. Responsible for creating API route function, validation input user data, and creating/closing database connection at the start/end of each request. 
2. Service layer. It's a place for all business logic and additional validation. 
3. Database layer. Responsible for creating actual SQL queries and executing them.


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
- Pydantic add PostgresDsn(WIP)


## Run project


```shell
docker-compose up app
```


### Run tests

```shell
docker-compose run --rm test
```


### Database migration

- autogenerate migration

    ```shell
    docker-compose run --rm alembic-autogenerate "Migration message"
    ```

- upgrade to latest version

    ```shell
    docker-compose run --rm alembic upgrade heads
    ```

- upgrade to previous version

    ```shell
    docker-compose run --rm alembic downgrade -1
    ```


### Run linters
- Run only check

    ```shell
    docker-compose run --rm lint-check
    ```
    
- Run linters and modify files

    ```shell
    docker-compose run --rm lint
    ```
