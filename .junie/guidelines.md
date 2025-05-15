# QuizMaster Developer Guidelines

This document provides concise guidance for new developers working on the QuizMaster project.

## Project Overview

QuizMaster is a Python-based application that uses virtual environments for dependency management. The project is currently in its initial setup phase.

## Project Structure

The recommended project structure is:

```
QuizMaster/
├── .venv/                  # Virtual environment (already set up)
├── .idea/                  # PyCharm IDE configuration
├── .junie/                 # Project guidelines and documentation
├── src/                    # Source code
│   └── quizmaster/         # Main package
│       ├── __init__.py
│       ├── models/         # Data models
│       ├── services/       # Business logic
│       └── utils/          # Utility functions
├── tests/                  # Test files
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── scripts/                # Utility scripts
├── requirements.txt        # Project dependencies
├── requirements-dev.txt    # Development dependencies
└── README.md               # Project documentation
```

## Setting Up the Environment

1. Create a virtual environment (already done):
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - On Windows: `.venv\Scripts\activate`
   - On macOS/Linux: `source .venv/bin/activate`

3. Install dependencies (once requirements.txt is created):
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```

## Running Tests

Once tests are implemented:

```bash
# Run all tests
pytest

# Run specific tests
pytest tests/unit/
pytest tests/integration/

# Run with coverage
pytest --cov=src
```

## Executing Scripts

Place utility scripts in the `scripts/` directory and make them executable:

```bash
# Example script execution
python scripts/example_script.py

# Or if made executable
./scripts/example_script.py
```

## Best Practices

1. **Code Style**: Follow PEP 8 guidelines. Use tools like `flake8` and `black` for linting and formatting.

2. **Documentation**: Document all modules, classes, and functions using docstrings.

3. **Testing**: Write tests for all new features. Aim for high test coverage.

4. **Version Control**:
   - Create feature branches from `main`
   - Write clear commit messages
   - Submit pull requests for code review

5. **Dependency Management**:
   - Add new dependencies to `requirements.txt`
   - Add development dependencies to `requirements-dev.txt`

6. **Error Handling**: Use appropriate exception handling and logging.

7. **Configuration**: Use environment variables or configuration files for settings.

## Development Workflow

1. Pull the latest changes from the main branch
2. Create a feature branch using the git_workflow.sh script:
   ```bash
   ./scripts/git_workflow.sh --name your-name
   ```
3. Implement your changes with tests
4. Run tests to ensure everything works
5. The git_workflow.sh script will automatically:
   - Create plan and tasks markdown files
   - Add your changes to git
   - Commit your work
   - Push your branch
   - Optionally create a pull request (with --pull-request flag)

### Git Workflow Commands

You can also manually execute the Git workflow commands:

```bash
# Step 1: Create and switch to a new branch
git checkout -b feature/{your-name}/{yyyy-MM-dd_hh-mm}

# Step 2: Create plan and tasks markdown files
touch plan-{yyyy-MM-dd_hh-mm}.md
touch tasks-{yyyy-MM-dd_hh-mm}.md

# Step 3: Add your work to git
git add .

# Step 4: Commit your work
git commit -m "Completed tasks from session {yyyy-MM-dd_hh-mm}"

# Step 5: Push your branch
git push origin feature/{your-name}/{yyyy-MM-dd_hh-mm}

# (Optional) Step 6: Create a Pull Request via GitHub UI or CLI
gh pr create --title "Work from {yyyy-MM-dd_hh-mm}" --body "Tasks completed as per session guidelines"
```

Replace `{your-name}` and `{yyyy-MM-dd_hh-mm}` with your actual name and timestamp of the session start.
