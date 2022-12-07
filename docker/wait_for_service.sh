#!/bin/bash

service_name="${SERVICE_NAME:=NO SERVICE}"
sleep_time="${SLEEP_TIME:=3}"
service_timeout="${SERVICE_TIMEOUT:=3}"

while ! (timeout "$service_timeout" bash -c "</dev/tcp/${SERVICE_HOST}/${SERVICE_PORT}") &> /dev/null;
do
    echo waiting for "$service_name" to start...;
    sleep "$sleep_time";
done;