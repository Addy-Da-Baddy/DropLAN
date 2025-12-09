#!/usr/bin/env python3
"""
DropLAN CLI - Command Line Interface for DropLAN
"""

import os
import sys
import webbrowser
import time
import subprocess
import socket
from pathlib import Path

PYTHON_ENTRY = Path(__file__).parent / "backend" / "app.py"


def find_free_port(start=5001, end=5100):
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start


def get_lan_ip():
    """Get LAN IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None


def main():
    port = find_free_port()
    lan_ip = get_lan_ip()
    
    print(f"\n[DropLAN] Starting server...")
    print(f"─────────────────────────────────────")
    print(f"  Local:   http://localhost:{port}/LAN_Drop")
    if lan_ip:
        print(f"  Network: http://{lan_ip}:{port}/LAN_Drop")
    print(f"─────────────────────────────────────")
    print(f"  Scan the QR code in the app to connect mobile devices")
    print(f"  Press Ctrl+C to stop\n")
    
    env = os.environ.copy()
    process = subprocess.Popen([sys.executable, str(PYTHON_ENTRY), str(port)], env=env)
    time.sleep(2)
    
    url = f"http://localhost:{port}/LAN_Drop"
    webbrowser.open(url)
    
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n[DropLAN] Stopping server...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("[DropLAN] Server stopped.")


if __name__ == "__main__":
    main()
