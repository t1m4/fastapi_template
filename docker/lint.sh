#!/bin/bash

mypy app
black app tests
flake8 app tests
isort app tests
