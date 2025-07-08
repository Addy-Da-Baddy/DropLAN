#!/bin/bash

# DropLAN Installation Script
# Run this to install DropLAN on your system

set -e

echo "DropLAN Installation Script"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Found Python $python_version"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip first."
    exit 1
fi

echo "📦 Installing DropLAN..."

# Install from current directory (for development) or from git
if [ -f "setup.py" ]; then
    echo "Installing from local directory..."
    pip3 install --user -e .
else
    echo "🔗 Installing from GitHub..."
    pip3 install --user git+https://github.com/Addy-Da-Baddy/DropLAN.git
fi

echo "DropLAN installed successfully!"
echo ""
echo "You can now run DropLAN with:"
echo "   droplan"
echo ""
echo "For help, run:"
echo "   droplan help"
echo ""
echo "Make sure ~/.local/bin is in your PATH"
echo "   Add this to your shell config (~/.bashrc, ~/.zshrc, etc.):"
echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
echo ""
echo "🌐 Once running, DropLAN will be available at:"
echo "   http://localhost:5000/LAN_Drop"
