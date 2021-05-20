#!/bin/bash

source .env
docker build -t wellness-bot:latest \
    -f docker/arm/Dockerfile \
    --no-cache .
