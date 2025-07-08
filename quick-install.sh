#!/bin/bash

# DropLAN Quick Install Script
# This script installs DropLAN directly from GitHub

set -e

echo "DropLAN Quick Install"
echo "========================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8+ first."
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "   macOS: brew install python"
    echo "   Windows: Download from python.org"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Found Python $python_version"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip first."
    echo "   Ubuntu/Debian: sudo apt install python3-pip"
    echo "   macOS: curl https://bootstrap.pypa.io/get-pip.py | python3"
    exit 1
fi

echo "📦 Installing DropLAN from GitHub..."

# Install DropLAN
pip3 install --user git+https://github.com/Addy-Da-Baddy/DropLAN.git

echo ""
echo "DropLAN installed successfully!"
echo ""
echo "Start DropLAN with:"
echo "   droplan"
echo ""
echo "Get help with:"
echo "   droplan help"
echo ""
echo "If 'droplan' command is not found, add ~/.local/bin to your PATH:"
echo "   echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
echo "   source ~/.bashrc"
echo ""
echo "🌐 DropLAN will run at: http://localhost:5000/LAN_Drop"
