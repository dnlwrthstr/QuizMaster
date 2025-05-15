# Setting Up Your Project on GitHub

This guide will walk you through the process of creating a GitHub repository for your QuizMaster project and pushing your local code to it.

## Prerequisites

1. A GitHub account
2. Git installed on your local machine
3. Basic familiarity with Git commands

## Step 1: Create a New Repository on GitHub

1. Log in to your GitHub account
2. Click on the "+" icon in the top-right corner and select "New repository"
3. Enter "QuizMaster" as the repository name
4. Add a description (optional): "A Python-based quiz application"
5. Choose whether the repository should be public or private
6. Do NOT initialize the repository with a README, .gitignore, or license (we'll push our existing code)
7. Click "Create repository"

## Step 2: Initialize Git in Your Local Project

Open a terminal and navigate to your project directory, then run:

```bash
# Initialize a new Git repository
git init

# Create a .gitignore file to exclude unnecessary files
```

## Step 3: Create a .gitignore File

Create a `.gitignore` file in your project root with the following content:

```
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
```

## Step 4: Add and Commit Your Files

```bash
# Add all files to staging
git add .

# Commit the files
git commit -m "Initial commit"
```

## Step 5: Connect and Push to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```bash
# Add the remote repository
git remote add origin https://github.com/YOUR_USERNAME/QuizMaster.git

# Push your code to GitHub
git push -u origin main
```

Note: If your default branch is named "master" instead of "main", use:

```bash
git push -u origin master
```

## Step 6: Verify Your Repository

1. Go to your GitHub account
2. Navigate to the QuizMaster repository
3. Confirm that your files have been successfully pushed

## Step 7: Install the Package in Development Mode

After cloning the repository, you should install the package in development mode to make imports work correctly:

```bash
# Activate your virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package in development mode
pip install -e .
```

This will install the package in a way that allows you to make changes to the code without having to reinstall it.

## Next Steps

Now that your project is on GitHub, you can:

1. Add collaborators to your project
2. Set up GitHub Actions for CI/CD
3. Create issues for tracking tasks
4. Use pull requests for code reviews
5. Set up branch protection rules

Refer to the QuizMaster Developer Guidelines for information on project structure, best practices, and workflow.
