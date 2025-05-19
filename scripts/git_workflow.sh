#!/bin/bash
# Script to automate the Git workflow for the QuizMaster project

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed. Please install git first."
    exit 1
fi

# Function to delete merged branches
delete_merged_branches() {
    echo "Deleting merged branches..."

    # Switch to main branch
    git checkout main

    # Update local repository
    git fetch -p

    # Get list of merged branches (excluding main and current branch)
    MERGED_BRANCHES=$(git branch --merged | grep -v "\*" | grep -v "main" | tr -d ' ')

    # Delete local merged branches
    if [ -n "$MERGED_BRANCHES" ]; then
        echo "Deleting local merged branches:"
        for branch in $MERGED_BRANCHES; do
            echo "  Deleting local branch: $branch"
            git branch -d "$branch"
        done
    else
        echo "No local merged branches to delete."
    fi

    # Delete remote merged branches
    REMOTE_MERGED_BRANCHES=$(git branch -r --merged origin/main | grep -v "main" | sed 's/origin\///')
    if [ -n "$REMOTE_MERGED_BRANCHES" ]; then
        echo "Deleting remote merged branches:"
        for branch in $REMOTE_MERGED_BRANCHES; do
            echo "  Deleting remote branch: $branch"
            git push origin --delete "$branch"
        done
    else
        echo "No remote merged branches to delete."
    fi

    echo "Branch cleanup completed."
}

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree &> /dev/null; then
    echo "Error: Not in a git repository. Please run this script from within a git repository."
    exit 1
fi

# Function to display usage information
usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -n, --name NAME       Your name (required for creating a new branch)"
    echo "  -h, --help            Display this help message"
    echo "  -p, --pull-request    Create a pull request (requires GitHub CLI)"
    echo "  -d, --delete-merged   Delete merged branches (local and remote)"
    echo ""
    echo "Examples:"
    echo "  $0 --name john                # Create a new branch and commit"
    echo "  $0 --delete-merged            # Delete merged branches"
    exit 1
}

# Parse command line arguments
NAME=""
CREATE_PR=false
DELETE_MERGED=false

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
        -d|--delete-merged)
            DELETE_MERGED=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# If delete-merged option is specified, delete merged branches and exit
if [ "$DELETE_MERGED" = true ]; then
    delete_merged_branches
    exit 0
fi

# Check if name is provided for creating a new branch
if [ -z "$NAME" ]; then
    echo "Error: Name is required when creating a new branch"
    usage
fi

# Generate timestamp in the required format
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")

# Step 1: Create and switch to a new branch
BRANCH_NAME="feature/${NAME}/${TIMESTAMP}"
echo "Creating and switching to branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME"

# Step 2: Create plan and tasks markdown files
# Ensure the doc/sessions directory exists
mkdir -p doc/sessions

PLAN_FILE="doc/sessions/plan-${TIMESTAMP}.md"
TASKS_FILE="doc/sessions/tasks-${TIMESTAMP}.md"

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
