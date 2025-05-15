#!/bin/bash
# Script to set up a GitHub repository for the QuizMaster project

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed. Please install git first."
    exit 1
fi

# Check if GitHub username is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <github_username>"
    echo "Example: $0 johndoe"
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME="QuizMaster"
DESCRIPTION="A Python-based quiz application"

echo "Setting up GitHub repository for $REPO_NAME..."

# Initialize git repository if not already initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
else
    echo "Git repository already initialized."
fi

# Create .gitignore file
echo "Creating .gitignore file..."
cat > .gitignore << EOL
# Python virtual environment
.venv/
venv/
ENV/

# Python bytecode
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
dist/
build/
*.egg-info/

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
coverage.xml
*.cover

# IDE specific files
.idea/
.vscode/
*.swp
*.swo

# OS specific files
.DS_Store
Thumbs.db
EOL

# Create README.md if it doesn't exist
if [ ! -f README.md ]; then
    echo "Creating README.md file..."
    cat > README.md << EOL
# QuizMaster

$DESCRIPTION

## Overview

QuizMaster is a Python-based application that uses virtual environments for dependency management.

## Getting Started

See the [Developer Guidelines](.junie/guidelines.md) for setup instructions and best practices.
EOL
fi

# Add files to git
echo "Adding files to git..."
git add .

# Commit files
echo "Committing files..."
git commit -m "Initial commit"

# Create GitHub repository using GitHub CLI if available
if command -v gh &> /dev/null; then
    echo "Creating GitHub repository using GitHub CLI..."
    gh repo create $REPO_NAME --description "$DESCRIPTION" --private --source=. --remote=origin
else
    echo "GitHub CLI not found. Please create the repository manually on GitHub."
    echo "Then run the following commands:"
    echo "git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo "git push -u origin main"
fi

echo "Setup complete!"
echo "If you created the repository manually, don't forget to push your code to GitHub."
echo "For more information, see .junie/github_setup.md"