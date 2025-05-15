#!/bin/bash
# Script to automate the Git workflow for the QuizMaster project

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed. Please install git first."
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree &> /dev/null; then
    echo "Error: Not in a git repository. Please run this script from within a git repository."
    exit 1
fi

# Function to display usage information
usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -n, --name NAME       Your name (required)"
    echo "  -h, --help            Display this help message"
    echo "  -p, --pull-request    Create a pull request (requires GitHub CLI)"
    echo ""
    echo "Example: $0 --name john"
    exit 1
}

# Parse command line arguments
NAME=""
CREATE_PR=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--name)
            NAME="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        -p|--pull-request)
            CREATE_PR=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Check if name is provided
if [ -z "$NAME" ]; then
    echo "Error: Name is required"
    usage
fi

# Generate timestamp in the required format
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")

# Step 1: Create and switch to a new branch
BRANCH_NAME="feature/${NAME}/${TIMESTAMP}"
echo "Creating and switching to branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME"

# Step 2: Create plan and tasks markdown files
PLAN_FILE="plan-${TIMESTAMP}.md"
TASKS_FILE="tasks-${TIMESTAMP}.md"

echo "Creating plan file: $PLAN_FILE"
touch "$PLAN_FILE"
echo "# Development Plan - $TIMESTAMP" > "$PLAN_FILE"
echo "" >> "$PLAN_FILE"
echo "## Objectives" >> "$PLAN_FILE"
echo "" >> "$PLAN_FILE"
echo "## Implementation Steps" >> "$PLAN_FILE"
echo "" >> "$PLAN_FILE"
echo "## Timeline" >> "$PLAN_FILE"

echo "Creating tasks file: $TASKS_FILE"
touch "$TASKS_FILE"
echo "# Tasks - $TIMESTAMP" > "$TASKS_FILE"
echo "" >> "$TASKS_FILE"
echo "## To Do" >> "$TASKS_FILE"
echo "" >> "$TASKS_FILE"
echo "## In Progress" >> "$TASKS_FILE"
echo "" >> "$TASKS_FILE"
echo "## Completed" >> "$TASKS_FILE"

# Step 3: Add your work to git
echo "Adding files to git"
git add .

# Step 4: Commit your work
echo "Committing your work"
git commit -m "Completed tasks from session ${TIMESTAMP}"

# Step 5: Push your branch
echo "Pushing branch to origin"
git push origin "$BRANCH_NAME"

# (Optional) Step 6: Create a Pull Request via GitHub CLI
if [ "$CREATE_PR" = true ]; then
    if command -v gh &> /dev/null; then
        echo "Creating a Pull Request"
        gh pr create --title "Work from ${TIMESTAMP}" --body "Tasks completed as per session guidelines"
    else
        echo "GitHub CLI (gh) is not installed. Skipping Pull Request creation."
        echo "To create a Pull Request manually, visit: https://github.com/YOUR_USERNAME/QuizMaster/pull/new/$BRANCH_NAME"
    fi
fi

echo "Workflow completed successfully!"
