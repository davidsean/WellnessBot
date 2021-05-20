#!/bin/bash

source .env

printf "%b" "${OKB}Building wellness-bot image${NC}\n"
docker build -t wellness-bot:latest \
    -f docker/arm/Dockerfile \
    --no-cache .
printf "%b" "${OKG} ✓ ${NC}image built\n"

printf "%b" "${OKB}Starting wellness-bot server${NC}\n"
docker run --env-file .env -d wellness-bot
printf "%b" "${OKG} ✓ ${NC}server container started\n"