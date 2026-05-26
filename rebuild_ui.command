#!/bin/bash
# CogniESL UI Rebuilder — double-click to update the web interface
# Run this whenever the UI has been updated (new features, design changes, etc.)

cd "$(dirname "$0")/webui"

echo "🔨 CogniESL UI Rebuilder"
echo "========================"
echo ""
echo "This will rebuild the web interface with the latest design."
echo "Takes about 30–60 seconds..."
echo ""

# Install any new frontend packages
echo "1. Checking frontend packages..."
npm install --silent
echo "   ✓ Packages ready"
echo ""

# Build the Next.js app
echo "2. Building UI..."
npm run build

if [ $? -eq 0 ]; then
    echo ""
    echo "========================"
    echo "✅ UI rebuilt successfully!"
    echo ""
    echo "Restart your server (double-click start_cogniesl.command)"
    echo "to see the new design."
else
    echo ""
    echo "========================"
    echo "❌ Build failed. Please contact support."
fi

echo ""
echo "Press any key to close..."
read -n 1
