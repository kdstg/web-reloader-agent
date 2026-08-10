#!/usr/bin/env bash
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install python packages
pip install -r requirements.txt

# Install playwright browsers specifically without trying restricted system package hooks
playwright install chromium