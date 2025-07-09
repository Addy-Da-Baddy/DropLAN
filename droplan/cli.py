#!/usr/bin/env python3
"""
DropLAN CLI - Command Line Interface for DropLAN
"""

import os
import sys
import webbrowser
import time
import signal
import subprocess
from pathlib import Path
import socket
import random

PYTHON_ENTRY = Path(__file__).parent / "backend" / "app.py"
DOCKER_IMAGE = "droplan"
DOCKER_CONTAINER = "droplan"


def is_port_in_use(port):
    # Check if port is in use on the host
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("0.0.0.0", port)) == 0

def is_port_used_by_docker(port):
    try:
        output = subprocess.check_output([
            "docker", "ps", "--format", "{{.Ports}}"
        ], universal_newlines=True)
        for line in output.splitlines():
            # Example: 0.0.0.0:5001->5000/tcp
            if f":{port}->" in line:
                return True
    except Exception:
        pass
    return False

def find_open_port(start=5000, end=6000):
    for port in range(start, end):
        if is_port_in_use(port):
            continue
        if is_port_used_by_docker(port):
            continue
        return port
    raise RuntimeError("No open port found in range")

def is_python_install():
    try:
        import flask
        import flask_socketio
        return PYTHON_ENTRY.exists()
    except ImportError:
        return False

def is_docker_available():
    try:
        subprocess.run(["docker", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

def run_python():
    print("[DropLAN] Launching native Python server on port 5000...")
    env = os.environ.copy()
    process = subprocess.Popen([sys.executable, str(PYTHON_ENTRY), "5000"], env=env)
    time.sleep(3)
    url = "http://localhost:5000/LAN_Drop"
    print(f"[DropLAN] Opening browser: {url}")
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

def run_docker():
    print("[DropLAN] Launching Docker container on port 5000...")
    subprocess.run(["docker", "rm", "-f", DOCKER_CONTAINER], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.Popen([
        "docker", "run", "--name", DOCKER_CONTAINER, "-d", "-p", "5000:5000", "-e", "DROPLAN_PORT=5000", DOCKER_IMAGE
    ])
    time.sleep(3)
    url = "http://localhost:5000/LAN_Drop"
    print(f"[DropLAN] Opening browser: {url}")
    webbrowser.open(url)
    print("[DropLAN] Docker container running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[DropLAN] Stopping Docker container...")
        subprocess.run(["docker", "rm", "-f", DOCKER_CONTAINER])
        print("[DropLAN] Container stopped.")

def main():
    if is_python_install():
        run_python()
    elif is_docker_available():
        run_docker()
    else:
        print("[DropLAN] ERROR: Neither Python nor Docker install found. Please install one of them.")
        sys.exit(1)

if __name__ == "__main__":
    main()
