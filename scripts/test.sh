#!/bin/bash

# script for dav

source .env

export DISCORD_TOKEN="$DISCORD_TOKEN"
export DISCORD_GUILD_ID="$DISCORD_GUILD_ID"
export CHANNEL_ID="$CHANNEL_ID"

python3 -m app