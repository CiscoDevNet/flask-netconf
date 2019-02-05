#!/bin/sh

# start redis
redis-server &

# start the web app
cd /app
python3 app.py
