#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip an install python requirements
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright system dependencies and Chromium browser binaries
playwright install --with-deps chromium