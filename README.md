# QuizMaster

A Python-based interactive quiz application

## Overview

QuizMaster is a Python-based application that provides an interactive quiz experience. It includes a chatbot that asks beginner-level Python programming questions, accepts user answers, and provides feedback on whether the responses are correct. The project uses virtual environments for dependency management.

## Project Structure

```
QuizMaster/
├── .venv/                  # Virtual environment
├── doc/                    # Documentation
│   └── sessions/           # Development session files (plan and tasks)
├── src/                    # Source code
│   └── quizmaster/         # Main package
│       ├── __init__.py
│       ├── main.py         # Entry point for the application
│       ├── models/         # Data models
│       │   └── quiz.py     # Quiz model for storing questions
│       ├── services/       # Business logic
│       │   └── quiz_bot.py # Interactive quiz bot implementation
│       └── utils/          # Utility functions
├── tests/                  # Test files
│   └── unit/               # Unit tests
│       ├── test_quiz.py    # Tests for Quiz model
│       └── test_quiz_bot.py# Tests for QuizBot
├── scripts/                # Utility scripts
└── .junie/                 # Project guidelines and documentation
```

## Getting Started

1. Clone this repository
2. Set up the virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install the package in development mode:
   ```bash
   pip install -e .
   ```
4. Install additional dependencies (if needed):
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development tools
   ```

## Running the Quiz Bot

After setting up the environment, you can run the interactive quiz bot:

```bash
# From the project root
python -m src.quizmaster.main
```

### Features

- Interactive chatbot that asks Python programming questions
- Multiple-choice questions with feedback on answers
- Option to quit the quiz at any time
- 5 preset beginner-level Python questions covering:
  - Variable declaration
  - Comments
  - Built-in functions
  - Data types
  - Operators

## Documentation

For more detailed information, see:

- [Developer Guidelines](.junie/guidelines.md) - Setup instructions and best practices
- [GitHub Setup Guide](.junie/github_setup.md) - Instructions for setting up this project on GitHub

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
