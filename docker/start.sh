#!/bin/bash

if [[ $ENVIRONMENT == "local" ]]; then
    bash docker/init.sh
    exec uvicorn --factory app.main:create_app --host 0.0.0.0 --port 8009 --reload
else
    exec uvicorn --factory app.main:create_app --host 0.0.0.0 --port 8000
fi
