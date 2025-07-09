#!/usr/bin/env bash

set -e

if [[ "$1" == "--docker" ]]; then
  echo "[DropLAN] Removing all pip installs..."
  pip uninstall -y droplan || true
  pip3 uninstall -y droplan || true
  echo "[DropLAN] Removing existing Docker container..."
  if command -v docker &>/dev/null; then
    docker rm -f droplan 2>/dev/null || true
    docker rmi -f droplan 2>/dev/null || true
  fi
  echo "Building DropLAN Docker image..."
  docker build -t droplan .
  # Install CLI wrapper for Docker
  mkdir -p "$HOME/.local/bin"
  ln -sf "$PWD/droplan-wrapper.sh" "$HOME/.local/bin/droplan"
  chmod +x "$HOME/.local/bin/droplan"
  echo "[DropLAN] Docker install complete! Type 'droplan' to launch Docker mode."
  exit 0
elif [[ "$1" == "--python" ]]; then
  echo "[DropLAN] Removing all Docker containers and images..."
  if command -v docker &>/dev/null; then
    docker rm -f droplan 2>/dev/null || true
    docker rmi -f droplan 2>/dev/null || true
  fi
  echo "[DropLAN] Uninstalling any previous pip installs..."
  pip uninstall -y droplan || true
  pip3 uninstall -y droplan || true
  echo "Installing DropLAN with pip..."
  pip install --user .
  # Install CLI for Python
  mkdir -p "$HOME/.local/bin"
  # Write a launcher that always runs the Python CLI
  cat > "$HOME/.local/bin/droplan" <<EOF
#!/usr/bin/env bash
exec python3 -m droplan.cli "$@"
EOF
  chmod +x "$HOME/.local/bin/droplan"
  echo "[DropLAN] Python install complete! Type 'droplan' to launch native mode."
  exit 0
else
  echo "Usage: $0 [--python|--docker]"
  echo "  --python   Install natively with Python (pip, no Docker)"
  echo "  --docker   Build Docker image only (no pip)"
  exit 1
fi

# Print PATH instructions if needed
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "[DropLAN] Add ~/.local/bin to your PATH to use 'droplan' from anywhere."
    if [ -n "$FISH_VERSION" ] || [ -n "$fish_user_paths" ]; then
        echo "  set -U fish_user_paths $HOME/.local/bin $fish_user_paths"
    else
        echo "  export PATH=\"$HOME/.local/bin:\$PATH\""
    fi
fi
