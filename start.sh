#!/bin/bash

echo ""
echo "============================================"
echo "   QuickPaste Debug Interface"
echo "============================================"
echo ""

# Navigate to quick_paste directory
cd quick_paste

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org"
    echo "Or use: brew install node (on macOS)"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
    echo ""
fi

echo "Starting server..."
echo ""

# Function to open URL in default browser based on OS
open_browser() {
    URL="http://localhost:8000/"
    
    # Detect the operating system
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open "$URL"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v xdg-open &> /dev/null; then
            xdg-open "$URL"
        elif command -v gnome-open &> /dev/null; then
            gnome-open "$URL"
        else
            echo "Please manually open: $URL"
        fi
    else
        echo "Please manually open: $URL"
    fi
}

# Wait a moment for server to initialize
(sleep 2 && open_browser) &

echo ""
echo "============================================"
echo "   Server is running!"
echo "   "
echo "   URL: http://localhost:8000/"
echo "   "
echo "   ✅ Works with ALL browsers"
echo "   ✅ Files save to data/to-be-scanned/"
echo "   "
echo "   Keep this terminal open!"
echo "   Press Ctrl+C to stop the server"
echo "============================================"
echo ""

# Run the Node.js server
node server.js