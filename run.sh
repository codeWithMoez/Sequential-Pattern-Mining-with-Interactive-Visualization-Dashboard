#!/bin/bash
# Unix/Linux/Mac Script to Run Sequential Pattern Mining Application

echo "========================================"
echo "Sequential Pattern Mining Dashboard"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ from python.org"
    exit 1
fi

echo "[1/3] Checking dependencies..."
if ! pip3 show fastapi &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
else
    echo "Dependencies already installed."
fi

echo ""
echo "[2/3] Starting Backend API..."
echo "Backend will run on http://localhost:8000"
echo ""

# Start backend in background
python3 backend/main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

echo ""
echo "[3/3] Starting Frontend Dashboard..."
echo "Frontend will open in your browser automatically."
echo ""
echo "========================================"
echo "READY! Press Ctrl+C to stop servers."
echo "========================================"
echo ""

# Start frontend (this will block)
streamlit run frontend/app.py

# Cleanup when frontend exits
kill $BACKEND_PID 2>/dev/null
