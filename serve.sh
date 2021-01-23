#!/bin/bash

cd "$(dirname "$(realpath "$0")")"
source .venv/bin/activate
python lichess-bot.py -u