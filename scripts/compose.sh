#!/bin/bash

source .env

# handle all non-zero exit status codes with a slack notification
trap 'handler $? $LINENO' ERR

handler () {
    printf "%b" "${FAIL} ✗ ${NC} dist build failed on line $2 with exit status $1\n"
}

printf "%b" "${OKB}Building wellness-bot for dev${NC}\n"
docker compose -f docker/docker-compose.yaml up
printf "%b" "${OKG} ✓ ${NC}containers active\n"
printf "%b" "${OKB}To teardown the containers run: docker compose -f docker/docker-compose.yaml down${NC}\n"
