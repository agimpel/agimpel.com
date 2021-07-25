#!/bin/bash

if [[ $# > 0 && $1 == 'prod' ]]; then
    echo "Starting server in production environment."
    eval "docker-compose -f prod.env up -d"
    exit 1;
else
    echo "Starting server in working environment."
    eval "docker-compose up -d"
    exit 1;
fi