#!/bin/bash

mypy app
black app tests --check
flake8 app tests
isort app tests --check-only
autoflake --remove-all-unused-imports --recursive --check  . | grep 'Unused imports/variables detected'
