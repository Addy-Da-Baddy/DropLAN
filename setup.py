#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

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
    ],
    entry_points={
        "console_scripts": [
            "droplan=droplan.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "droplan": ["templates/*.html", "static/*"],
    },
)
