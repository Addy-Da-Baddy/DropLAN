#!/usr/bin/env python3

from setuptools import setup, find_packages
import os
import sys

# Read README file
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except:
        return "DropLAN - Local Network File Sharing Tool"

setup(
    name="droplan",
    version="1.0.0",
    author="DropLAN Team",
    description="A local network file sharing tool with real-time sync",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Addy-Da-Baddy/DropLAN",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
    install_requires=[
        "flask>=2.0.0",
        "flask-cors>=3.0.0",
        "flask-socketio>=5.0.0",
        "qrcode[pil]>=7.0.0",
        "eventlet>=0.30.0",
        "python-socketio>=5.0.0",
        "APScheduler>=3.9.0",
        "netifaces>=0.11.0",
        "psutil>=5.8.0",
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "droplan=droplan.cli:main",
            "droplan-docker-wrapper=/home/addy/DropLAN/droplan-wrapper.sh"
        ],
    },
    include_package_data=True,
    package_data={
        "droplan": ["templates/*.html", "static/*", "../droplan-wrapper.sh"],
    },
)

if __name__ == "__main__":
    if "--docker" in sys.argv:
        print("To install and run with Docker, use:\n  docker build -t droplan . && docker run -it --rm -p 5000-6000:5000-6000 droplan")
        sys.exit(0)
    elif "--python" in sys.argv:
        print("To install with Python, use:\n  pip install . && droplan")
        sys.exit(0)

# NOTE: For LAN device discovery, the system must have the 'ping' command available (iputils-ping on Debian/Ubuntu).
# If running natively, install with: sudo apt install iputils-ping
