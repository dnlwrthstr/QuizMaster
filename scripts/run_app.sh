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

# Run the application
echo "Starting QuizMaster application..."
cd "$PROJECT_ROOT"
python -m quizmaster.main

# Deactivate the virtual environment when the application is stopped
trap "deactivate; echo 'Virtual environment deactivated.'" EXIT