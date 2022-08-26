#!/bin/sh
# ---
# help-text: Run a command inside the docker image
# image:
#   tag: hancock:$VG_DOCKER_UID
#   publish:
#     - "$PUBLISH"
#   volume:
#     - "$VG_APP_DIR:/usr/src/app"
# environment:
#   - "PUBLISH=5000"
# ---
set -eu
"${@:-bash}"
