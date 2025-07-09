#!/usr/bin/env bash
# droplan-wrapper.sh: Launch DropLAN via Docker if not available natively

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

# Robust LAN IP detection (first non-loopback, non-docker, non-virtual IPv4)
lan_ip=""
for ipdev in $(ip -o -4 addr show | awk '{print $2":"$4}'); do
    dev="${ipdev%%:*}"
    ip="${ipdev#*:}"
    ip="${ip%%/*}"
    case "$dev" in
        lo*|docker*|br-*|veth*|virbr*|vmnet*|zt*|tun*|tap*) continue;;
    esac
    if [ "$ip" != "127.0.0.1" ]; then
        lan_ip="$ip"
        break
    fi
    done
if [ -z "$lan_ip" ]; then
    lan_ip="Unknown"
fi

# Robust Wi-Fi SSID detection
wifi_name=""
if command -v nmcli &>/dev/null; then
    wifi_name=$(nmcli -t -f active,ssid dev wifi 2>/dev/null | grep '^yes:' | cut -d: -f2)
fi
if [ -z "$wifi_name" ] && command -v iwgetid &>/dev/null; then
    wifi_name=$(iwgetid -r 2>/dev/null)
fi
if [ -z "$wifi_name" ]; then
    wifi_name="Unknown Network"
fi

# Compose hostinfo only if valid
if [ "$lan_ip" != "Unknown" ] && [ "$wifi_name" != "Unknown Network" ]; then
    hostinfo="{\"ip\":\"$lan_ip\",\"wifi_name\":\"$wifi_name\",\"hostname\":\"$(hostname)\"}"
else
    hostinfo=""
    echo "[DropLAN] [WARN] Could not detect real LAN IP or Wi-Fi SSID. Network info in UI may show as 'Unknown'."
    echo "[DropLAN] Troubleshooting: Ensure you are connected to Wi-Fi and have 'nmcli' or 'iwgetid' installed."
fi

# Remove any existing container with the same name
if docker ps -a --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1
fi

# Launch Docker with hostinfo and port
if [ -n "$hostinfo" ]; then
    docker run --name "$CONTAINER_NAME" -d --network=host -e DROPLAN_HOST_NETINFO="$hostinfo" -e DROPLAN_PORT="$PORT" "$IMAGE_NAME"
else
    docker run --name "$CONTAINER_NAME" -d --network=host -e DROPLAN_PORT="$PORT" "$IMAGE_NAME"
fi

LAN_IP="$lan_ip"
URL="http://$LAN_IP:$PORT/"
echo "[DropLAN] Access on: $URL"
echo "[DropLAN] To stop: docker rm -f $CONTAINER_NAME"

# Open the default browser (Linux, fish compatible)
if command -v xdg-open &>/dev/null; then
    xdg-open "$URL" &>/dev/null &
fi

# Show logs interactively
exec docker logs -f "$CONTAINER_NAME"
