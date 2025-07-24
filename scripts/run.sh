#!/bin/bash

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[INFO] Starting Docker Compose..."
docker-compose -f "$ROOT_DIR/docker-compose.yml" up -d --build

API_URL="http://localhost:8000"
echo "[INFO] Waiting for API to start at $API_URL ..."
for i in {1..30}; do
    if curl -s $API_URL > /dev/null; then
        echo "[INFO] API is up and running!"
        break
    else
        echo "[INFO] API not available yet... ($i/30)"
        sleep 1
    fi
done

VIEWER_SCRIPT="$ROOT_DIR/services/viewer/viewer.sh"
if [ -f "$VIEWER_SCRIPT" ]; then
    echo "[INFO] Starting viewer.sh..."
    bash "$VIEWER_SCRIPT"
else
    echo "[ERROR] $VIEWER_SCRIPT not found!"
    exit 1
fi
