#!/usr/bin/env bash

# Remove existing droplan Docker container and image if present
if command -v docker &>/dev/null; then
    if docker ps -a --format '{{.Names}}' | grep -q '^droplan$'; then
        echo '[DropLAN] Removing existing Docker container...'
        docker rm -f droplan
    fi
    if docker images --format '{{.Repository}}' | grep -q '^droplan$'; then
        echo '[DropLAN] Removing existing Docker image...'
        docker rmi -f droplan
    fi
fi

if [[ "$1" == "--docker" ]]; then
  echo "Building DropLAN Docker image..."
  docker build -t droplan .
  # Do NOT run the container here
elif [[ "$1" == "--python" ]]; then
  echo "Installing DropLAN with pip..."
  pip install .
  # Do NOT run droplan here
else
  echo "Usage: $0 [--python|--docker]"
  echo "  --python   Install natively with Python (pip)"
  echo "  --docker   Build Docker image only"
  exit 1
fi

# Ensure ~/.local/bin exists
mkdir -p "$HOME/.local/bin"

# Install CLI wrapper for Docker (symlink droplan to droplan-wrapper.sh, portable for any user)
ln -sf "$PWD/droplan-wrapper.sh" "$HOME/.local/bin/droplan"
chmod +x "$HOME/.local/bin/droplan"

# Print instructions for user
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "[DropLAN] Add ~/.local/bin to your PATH to use 'droplan' from anywhere."
    if [ -n "$FISH_VERSION" ]; then
        echo "  set -U fish_user_paths $HOME/.local/bin $fish_user_paths"
    else
        echo "  export PATH=\"$HOME/.local/bin:\$PATH\""
    fi
fi

echo "[DropLAN] Installation complete! Type 'droplan' to start DropLAN."
