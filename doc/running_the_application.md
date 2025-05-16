# Running the QuizMaster Application

This document provides instructions on how to run the QuizMaster application, including both the backend (REST API) and the frontend.

## Prerequisites

- Python 3.8 or higher
- Virtual environment (already set up in the `.venv` directory)
- Node.js (for running the frontend server)

## Setting Up the Environment

1. Activate the virtual environment:
   - On Windows: `.venv\Scripts\activate`
   - On macOS/Linux: `source .venv/bin/activate`

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Backend (REST API)

The backend is a FastAPI application that runs on port 8091.

### Using the Run Script (Recommended)

The easiest way to run the backend is to use the provided run script:

```bash
# From the project root directory
./scripts/run_app.sh
```

This script will:
- Activate the virtual environment (or create one if it doesn't exist)
- Install dependencies if needed
- Start the FastAPI application on port 8091

### Manual Method

Alternatively, you can start the backend manually:

```bash
# From the project root directory
python -m quizmaster.main
```

This will start the FastAPI application using Uvicorn on `http://localhost:8091`.

You can verify the backend is running by accessing:
- API root: http://localhost:8091/api
- API documentation: http://localhost:8091/docs

## Running the Frontend

The frontend is served by a separate Node.js server on port 8090.

To start the frontend server:

```bash
# From the project root directory
cd frontend
node server.js
```

This will start a simple HTTP server on `http://localhost:8090`.

Once the frontend server is running, you can access the application at:

```
http://localhost:8090/
```

The frontend is configured to make API calls to the backend at `http://localhost:8091`.

## Port Configuration

- Backend (REST API): Port 8091
- Frontend: Port 8090

## Troubleshooting

If you encounter any issues:

1. Make sure the virtual environment is activated
2. Verify all dependencies are installed
3. Check that no other application is using ports 8090 or 8091
4. Ensure the API_BASE_URL in frontend/script.js is set to 'http://localhost:8091'
5. Make sure Node.js is installed for running the frontend server
