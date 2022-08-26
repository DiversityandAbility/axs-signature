#!/bin/sh
# ---
# help-text: Build the docker image
# ---
set -eu

docker build \
    --build-arg "UID=$VG_DOCKER_UID" \
    --build-arg "GID=$VG_DOCKER_GID" \
    --tag "hancock:$VG_DOCKER_UID" "$VG_APP_DIR"
