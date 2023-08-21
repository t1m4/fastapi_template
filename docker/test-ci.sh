#!/bin/bash


coverage run --data-file=artifacts/coverage -m pytest -s $@ 
coverage html --data-file=artifacts/coverage -d artifacts/html
