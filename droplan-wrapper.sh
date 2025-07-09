#!/usr/bin/env bash
# droplan-wrapper.sh: Launch DropLAN via Docker if not available natively

# Check if droplan Python CLI is available
if command -v droplan-python &>/dev/null; then
    exec droplan-python "$@"
    exit $?
fi

IMAGE_NAME="droplan"
CONTAINER_NAME="droplan"

# Find a free port starting from 5000
find_free_port() {
    local port=5000
    while ss -ltn | awk '{print $4}' | grep -q ":$port"; do
        port=$((port+1))
    done
    echo $port
}

PORT=$(find_free_port)

# Build image if not present
if ! docker images --format '{{.Repository}}' | grep -q "^$IMAGE_NAME$"; then
    docker build -t "$IMAGE_NAME" "$(dirname "$0")"
fi

# Remove any existing container with the same name
if docker ps -a --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1
fi

# Launch the container interactively so logs are shown

echo "[DropLAN] Launching Docker container on port $PORT..."
docker run --name "$CONTAINER_NAME" -d -p "$PORT:5000" -e DROPLAN_PORT=5000 "$IMAGE_NAME"

LAN_IP=$(hostname -I | awk '{print $1}')
URL="http://$LAN_IP:$PORT/"
echo "[DropLAN] Access on: $URL"
echo "[DropLAN] To stop: docker rm -f $CONTAINER_NAME"

# Open the default browser (Linux, fish compatible)
if command -v xdg-open &>/dev/null; then
    xdg-open "$URL" &>/dev/null &
fi

# Show logs interactively
exec docker logs -f "$CONTAINER_NAME"
