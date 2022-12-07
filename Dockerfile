FROM python:3.10-slim-bullseye as base

ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.1.13

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN poetry export --without-hashes --dev --output=requirements.txt
RUN pip install -r requirements.txt

COPY . /code

ENTRYPOINT ["docker/start.sh"]
