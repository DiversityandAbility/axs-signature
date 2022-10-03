#!/bin/sh
# ---
# help-text: Deploy to production
# ---
set -eu

echo "Building docker image..."
docker build \
    --build-arg UID=1003 \
    --build-arg GID=1003 \
    --tag "ghcr.io/diversityandability/hancock:latest" .

echo "Pushing images to GitHub..."
docker push "ghcr.io/diversityandability/hancock:latest"

echo "Running commands on remote server..."
ssh pistachio-sandbox 'bash -s' << EOF
    echo "Pulling latest version..."
    docker pull "ghcr.io/diversityandability/hancock:latest"
    
    echo "Stopping existing containers"
    docker container stop hancock
    docker container rm hancock

    echo "Spinning server back up..."
    docker run \
        --detach \
        --publish="60431:8000" \
        --env-file="/home/hancock/env" \
        --name=hancock \
        --restart=unless-stopped \
        --volume /home/hancock/data:/data \
        ghcr.io/diversityandability/hancock:latest
EOF
