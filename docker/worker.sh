#!/bin/bash

if [[ $ENVIRONMENT == "local" ]]; then

    # wait for Kafka
    SERVICE_NAME=Kafka SERVICE_HOST=${KAFKA_HOST} SERVICE_PORT=${KAFKA_PORT} ./docker/wait_for_service.sh

    # wait for database migration
    bash docker/init.sh

    # start worker with auto-reloading
    watchfiles "celery --app=app.worker.worker worker --loglevel=INFO" .
else
    celery --app app.worker.worker worker --loglevel=INFO
fi
