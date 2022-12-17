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
- Celery and Redis
- Sentry
- Kafka(WIP)


## Run application

- Using docker-compose
    ```shell
    docker-compose up app
    ```
- Using local shell
    
    1. Create virtual environment
        ```shell
        poetry shell
        ```
    2. Install all dependencies
        ```shell
        poetry install
        ```
    3. Start application
        ```shell
        docker/start.sh
        ```

## Run worker
 - Using docker-compose
    ```shell
    docker-compose up worker
    ```
## Run tests

 - Using docker-compose
    ```shell
    docker-compose run --rm test
    ```


## Database migration

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


## Run linters
- Run only check

    ```shell
    docker-compose run --rm lint-check
    ```
    
- Run linters and modify files

    ```shell
    docker-compose run --rm lint
    ```
