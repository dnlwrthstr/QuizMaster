#!/usr/bin/env python3
"""
Backend Test Script for the QuizMaster REST API.

This script tests all the REST API endpoints of the QuizMaster backend to ensure
they function correctly. It can be run as a standalone script or imported and used
in other test scripts.

Usage:
    python test_backend.py [--host HOST] [--port PORT] [--verbose]

Options:
    --host HOST     Specify the host address (default: localhost)
    --port PORT     Specify the port number (default: 8091)
    --verbose       Enable verbose output
    --no-start      Don't start the API server (assumes it's already running)
    --help          Show this help message and exit
"""

import argparse
import json
import os
import requests
import signal
import subprocess
import sys
import time
import platform
from pathlib import Path

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Default settings
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8091

class BackendTester:
    """Class for testing the QuizMaster backend REST API."""

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, verbose=False):
        """Initialize the tester with the given host and port."""
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.verbose = verbose
        self.api_process = None
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "total": 0
        }

    def print_success(self, message):
        """Print a success message in green."""
        print(f"{GREEN}✓ {message}{RESET}")
        if self.verbose:
            print()

    def print_error(self, message):
        """Print an error message in red."""
        print(f"{RED}✗ {message}{RESET}")
        if self.verbose:
            print()

    def print_info(self, message):
        """Print an info message in yellow."""
        print(f"{YELLOW}ℹ {message}{RESET}")
        if self.verbose:
            print()

    def print_header(self, message):
        """Print a header message in blue."""
        print(f"\n{BLUE}=== {message} ==={RESET}")

    def log_request(self, method, url, data=None):
        """Log the request details if verbose mode is enabled."""
        if self.verbose:
            print(f"Request: {method} {url}")
            if data:
                print(f"Data: {json.dumps(data, indent=2)}")

    def log_response(self, response):
        """Log the response details if verbose mode is enabled."""
        if self.verbose:
            print(f"Status: {response.status_code}")
            try:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            except json.JSONDecodeError:
                print(f"Response: {response.text}")

    def start_api_server(self):
        """Start the API server in a subprocess."""
        self.print_info("Starting API server...")

        # Get the project root directory
        script_dir = Path(__file__).parent
        project_root = script_dir.parent

        # Start the API in a subprocess
        # Use different process creation flags based on the platform
        if platform.system() == 'Windows':
            # Windows doesn't support preexec_fn, use CREATE_NEW_PROCESS_GROUP instead
            self.api_process = subprocess.Popen(
                ["python", "-m", "quizmaster.main"],
                cwd=project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            # Unix/Linux/Mac
            self.api_process = subprocess.Popen(
                ["python", "-m", "quizmaster.main"],
                cwd=project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid  # Create a new process group
            )

        # Wait for the API to become available
        if not self.wait_for_api():
            # Kill the API process if it didn't start properly
            self.stop_api_server()
            self.print_error("Failed to start API server")
            sys.exit(1)

    def stop_api_server(self):
        """Stop the API server subprocess."""
        if self.api_process:
            self.print_info("Stopping API server...")
            if platform.system() == 'Windows':
                # Windows uses a different approach to terminate process groups
                self.api_process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                # Unix/Linux/Mac
                os.killpg(os.getpgid(self.api_process.pid), signal.SIGTERM)
            self.api_process.wait()
            self.api_process = None

    def wait_for_api(self, max_attempts=10, delay=1):
        """Wait for the API to become available."""
        self.print_info("Waiting for API to start...")
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{self.base_url}/api")
                if response.status_code == 200:
                    self.print_success("API is available")
                    return True
            except requests.exceptions.RequestException:
                pass

            time.sleep(delay)

        self.print_error(f"API did not become available after {max_attempts} attempts")
        return False

    def run_test(self, test_func, *args, **kwargs):
        """Run a test function and track the result."""
        self.test_results["total"] += 1
        result = test_func(*args, **kwargs)
        if result is not None and result is not False:
            self.test_results["passed"] += 1
        else:
            self.test_results["failed"] += 1
        return result

    def test_api_root(self):
        """Test the API root endpoint."""
        self.print_header("Testing API Root Endpoint")
        try:
            url = f"{self.base_url}/api"
            self.log_request("GET", url)

            response = requests.get(url)
            self.log_response(response)

            if response.status_code == 200 and "Welcome to QuizMaster API" in response.text:
                self.print_success("API root endpoint is working")
                return True
            else:
                self.print_error(f"API root endpoint returned unexpected response: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            self.print_error(f"Failed to connect to API: {e}")
            return False

    def test_get_quizzes(self):
        """Test getting all quizzes."""
        self.print_header("Testing GET /quizzes Endpoint")
        try:
            url = f"{self.base_url}/quizzes"
            self.log_request("GET", url)

            response = requests.get(url)
            self.log_response(response)

            if response.status_code == 200:
                quizzes = response.json()
                self.print_success(f"Retrieved {len(quizzes)} quizzes")
                return True
            else:
                self.print_error(f"Failed to get quizzes: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            self.print_error(f"Failed to connect to API: {e}")
            return False

    def test_create_quiz(self):
        """Test creating a new quiz."""
        self.print_header("Testing POST /quizzes Endpoint")
        try:
            url = f"{self.base_url}/quizzes"
            quiz_data = {
                "title": "Test Quiz",
                "description": "A quiz created by the test script"
            }
            self.log_request("POST", url, quiz_data)

            response = requests.post(url, json=quiz_data)
            self.log_response(response)

            if response.status_code == 201:
                quiz = response.json()
                self.print_success(f"Created quiz with ID: {quiz['id']}")
                return quiz['id']
            else:
                self.print_error(f"Failed to create quiz: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            self.print_error(f"Failed to connect to API: {e}")
            return None

    def test_get_quiz(self, quiz_id):
        """Test getting a quiz by ID."""
        self.print_header(f"Testing GET /quizzes/{quiz_id} Endpoint")
        try:
            url = f"{self.base_url}/quizzes/{quiz_id}"
            self.log_request("GET", url)

            response = requests.get(url)
            self.log_response(response)

            if response.status_code == 200:
                quiz = response.json()
                self.print_success(f"Retrieved quiz {quiz_id}: {quiz['title']}")
                return True
            else:
                self.print_error(f"Failed to get quiz: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            self.print_error(f"Failed to connect to API: {e}")
            return False

    def test_add_question(self, quiz_id):
        """Test adding a question to a quiz."""
        self.print_header(f"Testing POST /quizzes/{quiz_id}/questions Endpoint")
        try:
            url = f"{self.base_url}/quizzes/{quiz_id}/questions"
            question_data = {
                "text": "What is the capital of France?",
                "answers": ["Paris", "London", "Berlin", "Madrid"],
                "correct_answer_index": 0
            }
            self.log_request("POST", url, question_data)

            response = requests.post(url, json=question_data)
            self.log_response(response)

            if response.status_code == 200:
                self.print_success(f"Added question to quiz {quiz_id}")
                return 0  # Return the question ID (first question has ID 0)
            else:
                self.print_error(f"Failed to add question: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            self.print_error(f"Failed to connect to API: {e}")
            return None

    def test_get_question(self, quiz_id, question_id):
        """Test getting a question by ID."""
        self.print_header(f"Testing GET /quizzes/{quiz_id}/questions/{question_id} Endpoint")
        try:
            url = f"{self.base_url}/quizzes/{quiz_id}/questions/{question_id}"
            self.log_request("GET", url)

            response = requests.get(url)
            self.log_response(response)

            if response.status_code == 200:
                question = response.json()
                self.print_success(f"Retrieved question {question_id}: {question['text']}")
                return True
            else:
                self.print_error(f"Failed to get question: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            self.print_error(f"Failed to connect to API: {e}")
            return False

    def test_submit_answer(self, quiz_id, question_id, answer_index):
        """Test submitting an answer to a question."""
        self.print_header(f"Testing POST /quizzes/{quiz_id}/questions/{question_id}/submit Endpoint")
        try:
            url = f"{self.base_url}/quizzes/{quiz_id}/questions/{question_id}/submit"
            submission_data = {
                "answer_index": answer_index
            }
            self.log_request("POST", url, submission_data)

            response = requests.post(url, json=submission_data)
            self.log_response(response)

            if response.status_code == 200:
                result = response.json()
                if result["is_correct"]:
                    self.print_success(f"Submitted correct answer: {result['message']}")
                else:
                    self.print_info(f"Submitted incorrect answer: {result['message']} (This is expected behavior, not a test failure)")
                return True
            else:
                self.print_error(f"Failed to submit answer: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            self.print_error(f"Failed to connect to API: {e}")
            return False

    def test_init_default_quiz(self):
        """Test initializing the default quiz."""
        self.print_header("Testing POST /init-default-quiz Endpoint")
        try:
            url = f"{self.base_url}/init-default-quiz"
            self.log_request("POST", url)

            response = requests.post(url)
            self.log_response(response)

            if response.status_code == 200:
                quiz = response.json()
                self.print_success(f"Initialized default quiz with ID: {quiz['id']}")
                return quiz['id']
            else:
                self.print_error(f"Failed to initialize default quiz: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            self.print_error(f"Failed to connect to API: {e}")
            return None

    def run_all_tests(self):
        """Run all API tests."""
        self.print_header("Starting Backend Tests")

        # Test API root
        if not self.run_test(self.test_api_root):
            return False

        # Test getting all quizzes
        self.run_test(self.test_get_quizzes)

        # Test creating a quiz
        quiz_id = self.run_test(self.test_create_quiz)
        if quiz_id is None:
            return False

        # Test getting the quiz
        if not self.run_test(self.test_get_quiz, quiz_id):
            return False

        # Test adding a question
        question_id = self.run_test(self.test_add_question, quiz_id)
        if question_id is None:
            return False

        # Test getting the question
        if not self.run_test(self.test_get_question, quiz_id, question_id):
            return False

        # Test submitting a correct answer
        if not self.run_test(self.test_submit_answer, quiz_id, question_id, 0):
            return False

        # Test submitting an incorrect answer
        self.run_test(self.test_submit_answer, quiz_id, question_id, 1)

        # Test initializing the default quiz
        default_quiz_id = self.run_test(self.test_init_default_quiz)
        if default_quiz_id is None:
            return False

        # Test getting the default quiz
        self.run_test(self.test_get_quiz, default_quiz_id)

        # Print test summary
        self.print_test_summary()

        return self.test_results["failed"] == 0

    def print_test_summary(self):
        """Print a summary of the test results."""
        self.print_header("Test Summary")
        print(f"Total tests: {self.test_results['total']}")
        print(f"Passed: {GREEN}{self.test_results['passed']}{RESET}")
        print(f"Failed: {RED}{self.test_results['failed']}{RESET}")

        if self.test_results["failed"] == 0:
            self.print_success("All tests passed!")
        else:
            self.print_error(f"{self.test_results['failed']} tests failed!")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test the QuizMaster backend REST API.")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"Host address (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port number (default: {DEFAULT_PORT})")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--no-start", action="store_true", help="Don't start the API server (assumes it's already running)")
    return parser.parse_args()


def main():
    """Main function to run the backend tests."""
    args = parse_arguments()

    tester = BackendTester(host=args.host, port=args.port, verbose=args.verbose)

    # Check if the API is already running
    try:
        response = requests.get(f"http://{args.host}:{args.port}/api")
        tester.print_info("API is already running, proceeding with tests")
        success = tester.run_all_tests()
    except requests.exceptions.RequestException:
        if args.no_start:
            tester.print_error("API is not running and --no-start option is set")
            return 1

        tester.print_info("API is not running, attempting to start it...")
        tester.start_api_server()

        try:
            success = tester.run_all_tests()
        finally:
            tester.stop_api_server()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
