#!/bin/bash

if [[ $ENVIRONMENT == "local" ]]; then
    exec uvicorn --factory app.main:create_app --host 0.0.0.0 --port 8000 --reload
else
    exec uvicorn --factory app.main:create_app --host 0.0.0.0 --port 8000 --workers 4
fi
