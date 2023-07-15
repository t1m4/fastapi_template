FROM python:3.10-slim-bullseye as base

ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.2.2

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . /code

ENTRYPOINT ["docker/start.sh"]
