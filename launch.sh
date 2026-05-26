#!/bin/bash

# CogniESL Server Launcher
# This script kills any process on port 8080, installs dependencies, and launches the server

cd "$(dirname "$0")"

echo "🚀 CogniESL Server Launcher"
echo "================================"
echo ""

# Kill any process on port 8080
echo "1. Checking for processes on port 8080..."
if lsof -ti :8080 > /dev/null 2>&1; then
    echo "   Found process on port 8080. Killing it..."
    lsof -ti :8080 | xargs kill -9 2>/dev/null
    sleep 1
    echo "   ✓ Killed"
else
    echo "   ✓ Port 8080 is free"
fi

echo ""
echo "2. Installing dependencies..."
pip3 install --break-system-packages -q -r requirements.txt
if [ $? -eq 0 ]; then
    echo "   ✓ Dependencies installed"
else
    echo "   ⚠️  Dependency installation had issues (likely network)"
    echo "   Continuing anyway..."
fi

echo ""
echo "3. Launching CogniESL server on http://localhost:8080"
echo "================================"
echo ""

python3 server.py
