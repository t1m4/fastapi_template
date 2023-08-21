#!/bin/bash

if [[ $ENVIRONMENT == "local" ]]; then
    # start worker with auto-reloading
    watchfiles "celery --app=app.worker.worker worker --loglevel=INFO" .
else
    celery --app app.worker.worker worker --loglevel=INFO
fi
