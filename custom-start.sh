#! /usr/bin/env sh
set -e
# echo "Starting up..."
# # copied from https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/master/docker-images/start.sh

# if [ -f /app/app/main.py ]; then
#     DEFAULT_MODULE_NAME=app.main
# elif [ -f /app/main.py ]; then
#     DEFAULT_MODULE_NAME=main
# fi
# echo "DEFAULT_MODULE_NAME=$DEFAULT_MODULE_NAME"
# MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
# echo "MODULE_NAME=$MODULE_NAME"
# VARIABLE_NAME=${VARIABLE_NAME:-app}
# echo "VARIABLE_NAME=$VARIABLE_NAME"
# export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

# if [ -f /app/gunicorn_conf.py ]; then
#     DEFAULT_GUNICORN_CONF=/app/gunicorn_conf.py
# elif [ -f /app/app/gunicorn_conf.py ]; then
#     DEFAULT_GUNICORN_CONF=/app/app/gunicorn_conf.py
# else
#     DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
# fi
# echo "DEFAULT_GUNICORN_CONF=$DEFAULT_GUNICORN_CONF"
# export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
# echo "GUNICORN_CONF=$GUNICORN_CONF"
# export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}
# echo "WORKER_CLASS=$WORKER_CLASS"

# # If there's a prestart.sh script in the /app directory or other path specified, run it before starting
# PRE_START_PATH=${PRE_START_PATH:-/app/prestart.sh}
# echo "Checking for script in $PRE_START_PATH"
# if [ -f $PRE_START_PATH ] ; then
#     echo "Running script $PRE_START_PATH"
#     . "$PRE_START_PATH"
# else 
#     echo "There is no script $PRE_START_PATH"
# fi

# # Start Gunicorn
# echo "Starting gunicorn..."
# gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE"
gunicorn -k "uvicorn.workers.UvicornWorker" -c "/gunicorn_conf.py" "app:main"
