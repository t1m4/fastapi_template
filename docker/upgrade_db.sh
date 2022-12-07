#!/bin/bash

SERVICE_NAME=Postgresql SERVICE_HOST=${POSTGRES_HOST} SERVICE_PORT=${POSTGRES_PORT} ./docker/wait_for_service.sh

alembic upgrade heads

