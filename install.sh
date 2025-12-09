#!/usr/bin/env bash
set -e

echo "[DropLAN] Installing dependencies..."
pip3 install --user -r requirements.txt

echo "[DropLAN] Setting up CLI..."
mkdir -p "$HOME/.local/bin"

cat > "$HOME/.local/bin/droplan" <<EOF
#!/usr/bin/env bash
exec python3 "$(cd "$(dirname "$0")" && pwd)/../../../$(pwd)/droplan/cli.py" "\$@"
EOF

# Create proper symlink approach
cat > "$HOME/.local/bin/droplan" <<EOF
#!/usr/bin/env bash
cd "$PWD"
exec python3 -m droplan.cli "\$@"
EOF

chmod +x "$HOME/.local/bin/droplan"

echo ""
echo "[DropLAN] Installation complete!"
echo ""
echo "Make sure ~/.local/bin is in your PATH:"
echo "  bash/zsh: export PATH=\"\$HOME/.local/bin:\$PATH\""
echo "  fish:     set -U fish_user_paths \$HOME/.local/bin \$fish_user_paths"
echo ""
echo "Then run: droplan"
