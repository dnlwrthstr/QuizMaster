# QuizMaster Frontend

This is the frontend application for QuizMaster, a quiz creation and management system. The frontend is built using HTML, CSS, and JavaScript without any UI libraries or frameworks.

## Overview

The QuizMaster frontend provides a user interface for:

- Viewing a list of available quizzes
- Creating new quizzes
- Adding questions to quizzes
- Taking quizzes and receiving feedback on answers

## Structure

The frontend consists of three main files:

- `index.html`: The main HTML structure of the application
- `styles.css`: CSS styles for the application
- `script.js`: JavaScript code for interacting with the backend API and handling user interactions

## Features

### Quiz List

The home page displays a list of all available quizzes. Users can:

- View all quizzes
- Initialize a default Python quiz
- Create a new quiz
- View details of a specific quiz

### Quiz Creation

Users can create new quizzes by providing:

- Quiz title
- Quiz description (optional)

### Question Management

For each quiz, users can:

- Add new questions
- Specify multiple answer options for each question
- Designate the correct answer

### Quiz Taking

Users can:

- Start a quiz
- Answer questions one by one
- Receive immediate feedback on their answers
- See their final score at the end of the quiz

## API Integration

The frontend communicates with the backend API using fetch requests. The main API endpoints used are:

- `GET /quizzes`: Fetch all quizzes
- `GET /quizzes/{quiz_id}`: Fetch a specific quiz
- `POST /quizzes`: Create a new quiz
- `POST /quizzes/{quiz_id}/questions`: Add a question to a quiz
- `POST /quizzes/{quiz_id}/questions/{question_id}/submit`: Submit an answer to a question
- `POST /init-default-quiz`: Initialize the default Python quiz

## Usage

1. Start the backend server (the QuizMaster FastAPI application)
2. Access the application at `http://localhost:8091`
3. Use the navigation menu to switch between viewing quizzes and creating new ones

## Development

To modify the frontend:

1. Edit the HTML, CSS, or JavaScript files as needed
2. Refresh the browser to see your changes

No build process is required as the application uses vanilla HTML, CSS, and JavaScript.