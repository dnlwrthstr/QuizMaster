#!/bin/bash

# Script to run the QuizMaster FastAPI application
# This script activates the virtual environment and runs the application

# Exit on error
set -e

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the project root directory
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Activate the virtual environment
if [ -d "$PROJECT_ROOT/.venv" ]; then
    echo "Activating virtual environment..."
    source "$PROJECT_ROOT/.venv/bin/activate"
else
    echo "Virtual environment not found. Creating one..."
    python -m venv "$PROJECT_ROOT/.venv"
    source "$PROJECT_ROOT/.venv/bin/activate"
    echo "Installing dependencies..."
    pip install -r "$PROJECT_ROOT/requirements.txt"
    pip install -r "$PROJECT_ROOT/requirements-dev.txt"
    pip install -e "$PROJECT_ROOT"
fi

# Start the frontend server in the background
echo "Starting frontend server on port 8090..."
cd "$PROJECT_ROOT/frontend"
node server.js &
FRONTEND_PID=$!

# Run the backend application on port 8091
echo "Starting QuizMaster backend application on port 8091..."
cd "$PROJECT_ROOT"
python -m quizmaster.main

# Cleanup function to kill the frontend server when the script exits
cleanup() {
    echo "Stopping frontend server..."
    kill $FRONTEND_PID
    echo "Deactivating virtual environment..."
    deactivate
    echo "Cleanup complete."
}

# Register the cleanup function to run when the script exits
trap cleanup EXIT
EOFo 'Virtual environment deactivated.'" EXIT