#!/bin/sh
# ---
# help-text: Run the app in production mode
# ---
docker run \
    --interactive \
    --tty \
    --rm \
    --publish "$VG_PORT:8000" \
    --volume "$VG_APP_DIR/data:/data" \
    "hancock:$VG_DOCKER_UID"
