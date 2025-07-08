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

def get_droplan_dir():
    """Get the DropLAN installation directory"""
    return Path(__file__).parent

def start_server():
    """Start the DropLAN server"""
    droplan_dir = get_droplan_dir()
    backend_dir = droplan_dir / "backend"
    
    if not backend_dir.exists():
        print("Backend directory not found. Please reinstall DropLAN.")
        sys.exit(1)
    
    app_py = backend_dir / "app.py"
    if not app_py.exists():
        print("app.py not found. Please reinstall DropLAN.")
        sys.exit(1)
    
    try:
        print("Starting DropLAN server...")
        
        # Start the Flask server
        env = os.environ.copy()
        env["PYTHONPATH"] = str(backend_dir)
        
        process = subprocess.Popen(
            [sys.executable, str(app_py)],
            cwd=str(backend_dir),
            env=env
        )
        
        # Give the server time to start
        print("⏳ Waiting for server to start...")
        time.sleep(3)
        
        # Open browser
        url = "http://localhost:5000/LAN_Drop"
        print(f"🌐 Opening DropLAN in your browser: {url}")
        webbrowser.open(url)
        
        print("DropLAN is running!")
        print("Share files across devices on your local network")
        print("🔗 Other devices can access: http://YOUR_IP:5000/LAN_Drop")
        print("Make sure all devices are on the same Wi-Fi network")
        print("\nCommands:")
        print("   • Ctrl+C to stop the server")
        print("   • Check the web interface for QR code and network info")
        
        try:
            # Wait for the process and handle Ctrl+C
            process.wait()
        except KeyboardInterrupt:
            print("\nStopping DropLAN server...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            print("DropLAN stopped successfully!")
            
    except FileNotFoundError:
        print("Python not found. Please install Python 3.8+")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting DropLAN: {e}")
        sys.exit(1)

def show_help():
    """Show help information"""
    print("""
DropLAN - Local Network File Sharing

Usage:
    droplan              Start DropLAN server and open in browser
    droplan start        Start DropLAN server and open in browser
    droplan help         Show this help message
    droplan version      Show version information

Examples:
    # Start DropLAN
    droplan

    # Get help
    droplan help

Features:
    - File sharing across devices on same network
    - Real-time notes app with sync
    - QR code for easy device connection
    - WebSocket real-time updates
    
Network Setup:
    1. All devices must be on the same Wi-Fi network
    2. DropLAN will show your IP and generate QR code
    3. Other devices can:
       - Scan the QR code, OR
       - Go to http://YOUR_IP:5000/LAN_Drop, OR
       - Use the Network Sync section to manually enter IP address
""")

def show_version():
    """Show version information"""
    print("DropLAN v1.0.0")
    print("Local Network File Sharing Tool")

def main():
    """Main CLI entry point"""
    args = sys.argv[1:]
    
    if len(args) == 0 or (len(args) == 1 and args[0] == "start"):
        start_server()
    elif len(args) == 1 and args[0] == "help":
        show_help()
    elif len(args) == 1 and args[0] == "version":
        show_version()
    else:
        print("Unknown command. Use 'droplan help' for usage information.")
        sys.exit(1)

if __name__ == "__main__":
    main()
