#!/bin/bash

path=/home/futurist/the_first

#set -e
source $path/venv/bin/activate
python3 $path/user_bot/the_first.py &
python3 $path/main.py
