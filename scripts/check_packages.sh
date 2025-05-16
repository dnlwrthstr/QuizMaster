#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Check if the virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual environment not activated. Please check your .venv directory."
    exit 1
fi

# List the required packages
echo "Listing required packages:"
python -m pip list | grep -E "fastapi|uvicorn|pydantic"

# Exit with success
exit 0