#!/bin/bash
# CogniESL Startup Script — double-click to run
# Starts the server + prevents Mac from sleeping

cd "$(dirname "$0")"

# Prevent Mac sleep for 8 hours
caffeinate -d -t 28800 &
echo "✓ Sleep prevention active (8 hours)"

# Activate venv
source venv/bin/activate

# Install/update dependencies (handles any new packages added since last launch)
echo "✓ Checking dependencies..."
pip install -q -r requirements.txt

# Start server
echo "✓ Starting CogniESL server on port 8080..."
python server.py
