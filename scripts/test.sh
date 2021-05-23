#!/bin/bash

# script for dav

source .env

export DISCORD_TOKEN="$DISCORD_TOKEN"
export DISCORD_GUILD_ID="$DISCORD_GUILD_ID"
export CHANNEL_ID="$CHANNEL_ID"
export MONGO_PASS="$MONGO_PASS"
export MONGO_USER="$MONGO_USER"
export MONGO_PORT="$MONGO_PORT"
export MONGO_HOST=localhost

python3 -m app