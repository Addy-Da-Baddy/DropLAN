#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[DropLAN] Installing dependencies..."
pip3 install --user -r "$SCRIPT_DIR/requirements.txt"

echo "[DropLAN] Setting up CLI..."
mkdir -p "$HOME/.local/bin"

# Create the droplan launcher script
cat > "$HOME/.local/bin/droplan" <<EOF
#!/usr/bin/env bash
exec python3 "$SCRIPT_DIR/src/cli.py" "\$@"
EOF

chmod +x "$HOME/.local/bin/droplan"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "[DropLAN] Adding ~/.local/bin to your PATH..."
    
    # Detect shell and add to appropriate config
    SHELL_NAME=$(basename "$SHELL")
    case "$SHELL_NAME" in
        zsh)
            # Check for custom ZDOTDIR or common locations
            if [[ -n "$ZDOTDIR" && -f "$ZDOTDIR/.zshrc" ]]; then
                SHELL_RC="$ZDOTDIR/.zshrc"
            elif [[ -f "$HOME/.config/zsh/.zshrc" ]]; then
                SHELL_RC="$HOME/.config/zsh/.zshrc"
            else
                SHELL_RC="$HOME/.zshrc"
            fi
            ;;
        bash)
            if [[ -f "$HOME/.bash_profile" ]]; then
                SHELL_RC="$HOME/.bash_profile"
            else
                SHELL_RC="$HOME/.bashrc"
            fi
            ;;
        fish)
            # Fish uses a different method
            fish -c 'set -U fish_user_paths $HOME/.local/bin $fish_user_paths' 2>/dev/null || true
            SHELL_RC=""
            ;;
        *)
            SHELL_RC="$HOME/.profile"
            ;;
    esac
    
    if [[ -n "$SHELL_RC" ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        echo "[DropLAN] Added PATH to $SHELL_RC"
    fi
fi

echo ""
echo "════════════════════════════════════════════════"
echo "  ✅ DropLAN installed successfully!"
echo "════════════════════════════════════════════════"
echo ""
echo "  To start using droplan, either:"
echo "    1. Restart your terminal, OR"
echo "    2. Run: source ~/.zshrc (or your shell's rc file)"
echo ""
echo "  Then simply type: droplan"
echo ""
