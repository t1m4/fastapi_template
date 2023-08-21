FROM python:3.10-slim-bullseye as base

FROM base as app_builder
ENV PYTHONUNBUFFERED 1
ENV APP_DIR "/home/appuser/src"
ENV PATH="/tmp/env/bin:/home/appuser/.local/bin:${PATH}"
ENV PYTHONPATH=${APP_DIR}

# Update system
RUN apt-get update \
    && apt-get --no-install-recommends install -y gcc g++ python3-dev \
    && apt-get clean

# Add non-root user
RUN useradd --create-home appuser
USER appuser
WORKDIR ${APP_DIR}

# Install poetry and dependencies
COPY --chown=appuser ./poetry.lock ${APP_DIR}/poetry.lock
COPY --chown=appuser ./pyproject.toml ${APP_DIR}/pyproject.toml
RUN pip install -U pip==23.1.2 poetry==1.4.2 \
    && python -m venv /tmp/env \
    && . /tmp/env/bin/activate \
    && poetry install --without dev

FROM app_builder as app
COPY --chown=appuser app ${APP_DIR}/app
COPY --chown=appuser docker ${APP_DIR}/docker
ENTRYPOINT ["docker/start.sh"]


FROM app_builder as test
RUN . /tmp/env/bin/activate && poetry install --with dev,test
COPY --chown=appuser app ${APP_DIR}/app
COPY --chown=appuser tests ${APP_DIR}/tests
COPY --chown=appuser docker ${APP_DIR}/docker


FROM app_builder as migrations
RUN . /tmp/env/bin/activate && poetry install --with dev
COPY --chown=appuser app ${APP_DIR}/app
COPY --chown=appuser migrations ${APP_DIR}/migrations
COPY --chown=appuser alembic.ini ${APP_DIR}
CMD ["alembic", "upgrade", "head"]

