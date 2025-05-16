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

## Running the Application

### Interactive Quiz Bot (CLI)

After setting up the environment, you can run the interactive quiz bot:

```bash
# From the project root
python -m src.quizmaster.main
```

### REST API Server

QuizMaster now provides a REST API using FastAPI. To run the API server:

```bash
# From the project root
python -m src.quizmaster.main
```

The API server will start at http://localhost:8000. You can access the interactive API documentation at http://localhost:8000/docs.

## Features

### CLI Features

- Interactive chatbot that asks Python programming questions
- Multiple-choice questions with feedback on answers
- Option to quit the quiz at any time
- 5 preset beginner-level Python questions covering:
  - Variable declaration
  - Comments
  - Built-in functions
  - Data types
  - Operators

### API Features

- RESTful endpoints for quiz management
- JSON responses for easy frontend integration
- Interactive API documentation with Swagger UI
- Endpoints for creating quizzes, adding questions, and submitting answers

## API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Welcome message |
| GET | /quizzes | Get all quizzes |
| POST | /quizzes | Create a new quiz |
| GET | /quizzes/{quiz_id} | Get a specific quiz by ID |
| POST | /quizzes/{quiz_id}/questions | Add a question to a quiz |
| GET | /quizzes/{quiz_id}/questions/{question_id} | Get a specific question |
| POST | /quizzes/{quiz_id}/questions/{question_id}/submit | Submit an answer to a question |
| POST | /init-default-quiz | Initialize the default Python quiz |

### Example API Usage

#### Creating a Quiz

```bash
curl -X 'POST' \
  'http://localhost:8000/quizzes' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "My Custom Quiz",
  "description": "A quiz about various topics"
}'
```

#### Adding a Question

```bash
curl -X 'POST' \
  'http://localhost:8000/quizzes/0/questions' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "What is the capital of France?",
  "answers": ["London", "Paris", "Berlin", "Madrid"],
  "correct_answer_index": 1
}'
```

#### Submitting an Answer

```bash
curl -X 'POST' \
  'http://localhost:8000/quizzes/0/questions/0/submit' \
  -H 'Content-Type: application/json' \
  -d '{
  "answer_index": 1
}'
```

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
