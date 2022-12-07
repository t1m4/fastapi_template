#!/bin/bash

bash docker/upgrade_db.sh

coverage run -m pytest -s 