#!/bin/sh
# ---
# help-text: Bootstrap this project
# ---
set -eu

vg __init

PORT=$(python -c 'import socket; s=socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()')

echo "VG_DOCKER_GID=$(id -g)" >> "$VG_APP_DIR/.vantage"
echo "VG_DOCKER_UID=$(id -u)" >> "$VG_APP_DIR/.vantage"
echo "VG_DOCKER_NETWORK=hancock-$(id -u)" >> "$VG_APP_DIR/.vantage"
echo "VG_PORT=$PORT" >> "$VG_APP_DIR/.vantage"

docker network create "$(vg __env VG_DOCKER_NETWORK)" > /dev/null 2> /dev/null || true

vg __env DEBUG=1
vg __env SECRET_KEY=notasecret
vg __env FLASK_ENV=development
vg __env FLASK_APP=hancock

vg build
