#!/bin/bash

mypy app
black app tests
flake8 app tests
autoflake --remove-all-unused-imports --recursive --in-place app tests
isort app tests
