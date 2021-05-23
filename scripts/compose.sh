#!/bin/bash

source .env

# handle all non-zero exit status codes with a slack notification
trap 'handler $? $LINENO' ERR

handler () {
    printf "%b" "${FAIL} ✗ ${NC} dist build failed on line $2 with exit status $1\n"
}
# TODO: add context for arm64 vs x86 hosts (arm64 for deployment and x86 for dev)
printf "%b" "${OKB}Building wellness-bot for x86 host${NC}\n"
docker-compose -f docker/docker-compose.yaml up -d
printf "%b" "${OKG} ✓ ${NC}containers active\n"
printf "%b" "${OKB}To teardown the containers run: docker-compose -f docker/docker-compose.yaml -d down${NC}\n"
