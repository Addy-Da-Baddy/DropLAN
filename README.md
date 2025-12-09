# DropLAN

**Local network file sharing with a clean web interface**

![DropLAN Interface](screengrab.jpeg)

## Features

- **File Sharing** — Drag & drop files to share across devices
- **Real-time Notes** — Create and sync notes instantly  
- **QR Code** — Auto-generates QR code with your LAN IP for mobile devices
- **Auto IP Detection** — Works on macOS, Linux, and Unix
- **Live Sync** — WebSocket-powered updates
- **Cross-Platform** — Works on any device with a browser

## Installation

```bash
git clone https://github.com/Addy-Da-Baddy/DropLAN.git
cd DropLAN
chmod +x install.sh
./install.sh
```

Add `~/.local/bin` to your PATH if needed:
```bash
# bash/zsh
export PATH="$HOME/.local/bin:$PATH"

# fish
set -U fish_user_paths $HOME/.local/bin $fish_user_paths
```

## Usage

```bash
droplan
```

Output:
```
[DropLAN] Starting server...
─────────────────────────────────────
  Local:   http://localhost:5001/LAN_Drop
  Network: http://192.168.1.100:5001/LAN_Drop
─────────────────────────────────────
  Scan the QR code in the app to connect mobile devices
  Press Ctrl+C to stop
```

Open the app in your browser and scan the QR code with your phone to connect.

## Requirements

- Python 3.8+
- macOS, Linux, or Unix
- All devices on the same network

## Troubleshooting

**"Command not found: droplan"**  
Add `~/.local/bin` to your PATH and restart your terminal.

**"Connection refused"**  
Check if the port is in use. The app auto-selects an available port starting from 5001.

**Devices can't connect**  
All devices must be on the same Wi-Fi network. Check firewall settings.

## License

MIT — see [LICENSE](LICENSE)

---

**Made by Adriteyo Das**
