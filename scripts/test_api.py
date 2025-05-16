#!/usr/bin/env python3
"""
Test script for the QuizMaster REST API.
This script tests the basic functionality of the API endpoints.
"""

import requests
import json
import sys
import time
import subprocess
import os
import signal
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8091"

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def print_success(message):
    """Print a success message in green."""
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    """Print an error message in red."""
    print(f"{RED}✗ {message}{RESET}")

def print_info(message):
    """Print an info message in yellow."""
    print(f"{YELLOW}ℹ {message}{RESET}")

def test_api_root():
    """Test the API root endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/api")
        if response.status_code == 200 and "Welcome to QuizMaster API" in response.text:
            print_success("API root endpoint is working")
            return True
        else:
            print_error(f"API root endpoint returned unexpected response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to connect to API: {e}")
        return False

def test_create_quiz():
    """Test creating a new quiz."""
    try:
        quiz_data = {
            "title": "Test Quiz",
            "description": "A quiz created by the test script"
        }
        response = requests.post(f"{BASE_URL}/quizzes", json=quiz_data)
        if response.status_code == 201:
            quiz = response.json()
            print_success(f"Created quiz with ID: {quiz['id']}")
            return quiz['id']
        else:
            print_error(f"Failed to create quiz: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to connect to API: {e}")
        return None

def test_add_question(quiz_id):
    """Test adding a question to a quiz."""
    try:
        question_data = {
            "text": "What is the capital of France?",
            "answers": ["Paris", "London", "Berlin", "Madrid"],
            "correct_answer_index": 0
        }
        response = requests.post(f"{BASE_URL}/quizzes/{quiz_id}/questions", json=question_data)
        if response.status_code == 200:
            print_success(f"Added question to quiz {quiz_id}")
            return 0  # Return the question ID (first question has ID 0)
        else:
            print_error(f"Failed to add question: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to connect to API: {e}")
        return None

def test_get_quiz(quiz_id):
    """Test getting a quiz by ID."""
    try:
        response = requests.get(f"{BASE_URL}/quizzes/{quiz_id}")
        if response.status_code == 200:
            quiz = response.json()
            print_success(f"Retrieved quiz {quiz_id}: {quiz['title']}")
            return True
        else:
            print_error(f"Failed to get quiz: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to connect to API: {e}")
        return False

def test_get_question(quiz_id, question_id):
    """Test getting a question by ID."""
    try:
        response = requests.get(f"{BASE_URL}/quizzes/{quiz_id}/questions/{question_id}")
        if response.status_code == 200:
            question = response.json()
            print_success(f"Retrieved question {question_id}: {question['text']}")
            return True
        else:
            print_error(f"Failed to get question: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to connect to API: {e}")
        return False

def test_submit_answer(quiz_id, question_id, answer_index):
    """Test submitting an answer to a question."""
    try:
        submission_data = {
            "answer_index": answer_index
        }
        response = requests.post(
            f"{BASE_URL}/quizzes/{quiz_id}/questions/{question_id}/submit", 
            json=submission_data
        )
        if response.status_code == 200:
            result = response.json()
            if result["is_correct"]:
                print_success(f"Submitted correct answer: {result['message']}")
            else:
                print_info(f"Submitted incorrect answer: {result['message']}")
            return True
        else:
            print_error(f"Failed to submit answer: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to connect to API: {e}")
        return False

def test_init_default_quiz():
    """Test initializing the default quiz."""
    try:
        response = requests.post(f"{BASE_URL}/init-default-quiz")
        if response.status_code == 200:
            quiz = response.json()
            print_success(f"Initialized default quiz with ID: {quiz['id']}")
            return quiz['id']
        else:
            print_error(f"Failed to initialize default quiz: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to connect to API: {e}")
        return None

def test_get_quizzes():
    """Test getting all quizzes."""
    try:
        response = requests.get(f"{BASE_URL}/quizzes")
        if response.status_code == 200:
            quizzes = response.json()
            print_success(f"Retrieved {len(quizzes)} quizzes")
            return True
        else:
            print_error(f"Failed to get quizzes: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to connect to API: {e}")
        return False

def wait_for_api(max_attempts=10, delay=1):
    """Wait for the API to become available."""
    print_info("Waiting for API to start...")
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/api")
            if response.status_code == 200:
                print_success("API is available")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(delay)
    
    print_error(f"API did not become available after {max_attempts} attempts")
    return False

def run_tests():
    """Run all API tests."""
    print_info("Starting API tests...")
    
    # Test API root
    if not test_api_root():
        return False
    
    # Test getting all quizzes
    test_get_quizzes()
    
    # Test creating a quiz
    quiz_id = test_create_quiz()
    if quiz_id is None:
        return False
    
    # Test getting the quiz
    if not test_get_quiz(quiz_id):
        return False
    
    # Test adding a question
    question_id = test_add_question(quiz_id)
    if question_id is None:
        return False
    
    # Test getting the question
    if not test_get_question(quiz_id, question_id):
        return False
    
    # Test submitting a correct answer
    if not test_submit_answer(quiz_id, question_id, 0):
        return False
    
    # Test submitting an incorrect answer
    test_submit_answer(quiz_id, question_id, 1)
    
    # Test initializing the default quiz
    default_quiz_id = test_init_default_quiz()
    if default_quiz_id is None:
        return False
    
    # Test getting the default quiz
    test_get_quiz(default_quiz_id)
    
    print_success("All tests completed successfully!")
    return True

if __name__ == "__main__":
    # Check if the API is already running
    try:
        response = requests.get(f"{BASE_URL}/api")
        print_info("API is already running, proceeding with tests")
        run_tests()
    except requests.exceptions.RequestException:
        print_info("API is not running, attempting to start it...")
        
        # Get the project root directory
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        
        # Start the API in a subprocess
        api_process = subprocess.Popen(
            ["python", "-m", "quizmaster.main"],
            cwd=project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid  # Create a new process group
        )
        
        # Wait for the API to become available
        if wait_for_api():
            try:
                # Run the tests
                run_tests()
            finally:
                # Kill the API process
                print_info("Stopping API...")
                os.killpg(os.getpgid(api_process.pid), signal.SIGTERM)
                api_process.wait()
                print_info("API stopped")
        else:
            # Kill the API process if it didn't start properly
            os.killpg(os.getpgid(api_process.pid), signal.SIGTERM)
            api_process.wait()
            print_error("Failed to start API")
            sys.exit(1)