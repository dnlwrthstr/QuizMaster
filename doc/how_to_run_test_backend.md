# How to Run test_backend.py

The `test_backend.py` script is located in the `scripts` directory and is used to test all REST API endpoints of the QuizMaster backend. Here's how to run it:

## Basic Usage

1. Make sure you're in the project root directory
2. Activate the virtual environment:
   ```bash
   # On macOS/Linux
   source .venv/bin/activate
   
   # On Windows
   .venv\Scripts\activate
   ```
3. Run the script:
   ```bash
   python scripts/test_backend.py
   ```
   
   Or, since the script is executable:
   ```bash
   ./scripts/test_backend.py
   ```

## Command-Line Options

The script supports several command-line options:

- `--host HOST`: Specify the host address (default: localhost)
- `--port PORT`: Specify the port number (default: 8091)
- `--verbose`: Enable verbose output with detailed request/response information
- `--no-start`: Don't start the API server (assumes it's already running)
- `--help`: Show help message and exit

## Examples

1. Run with verbose output:
   ```bash
   ./scripts/test_backend.py --verbose
   ```

2. Connect to a server running on a different host/port:
   ```bash
   ./scripts/test_backend.py --host 192.168.1.100 --port 8000
   ```

3. Test against an already running server:
   ```bash
   ./scripts/test_backend.py --no-start
   ```

## Understanding Test Results

The script will automatically:
1. Check if the API server is running
2. Start the server if needed (unless `--no-start` is specified)
3. Run tests against all REST endpoints
4. Display a summary of test results
5. Stop the server if it was started by the script

When the script runs, it will display colored output:
- Green (✓): Indicates a successful test
- Red (✗): Indicates a failed test
- Yellow (ℹ): Provides informational messages

Note: When testing the answer submission endpoint, the script will test both correct and incorrect answers. An "incorrect answer" message is expected behavior and not a test failure.

If all tests pass, the script will exit with a status code of 0. If any tests fail, it will exit with a status code of 1.