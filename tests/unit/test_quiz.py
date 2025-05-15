"""
Unit tests for the Quiz model.
"""

import pytest

from quizmaster.models.quiz import Quiz


def test_quiz_initialization():
    """Test that a Quiz can be initialized with a title and description."""
    # Arrange & Act
    quiz = Quiz("Test Quiz", "A quiz for testing")
    
    # Assert
    assert quiz.title == "Test Quiz"
    assert quiz.description == "A quiz for testing"
    assert quiz.questions == []


def test_quiz_initialization_without_description():
    """Test that a Quiz can be initialized with just a title."""
    # Arrange & Act
    quiz = Quiz("Test Quiz")
    
    # Assert
    assert quiz.title == "Test Quiz"
    assert quiz.description == ""
    assert quiz.questions == []


def test_add_question():
    """Test that a question can be added to a Quiz."""
    # Arrange
    quiz = Quiz("Test Quiz")
    question = "What is the capital of France?"
    answers = ["London", "Paris", "Berlin", "Madrid"]
    correct_answer_index = 1
    
    # Act
    quiz.add_question(question, answers, correct_answer_index)
    
    # Assert
    assert len(quiz.questions) == 1
    assert quiz.questions[0]["question"] == question
    assert quiz.questions[0]["answers"] == answers
    assert quiz.questions[0]["correct_answer_index"] == correct_answer_index


def test_add_question_with_invalid_index():
    """Test that adding a question with an invalid index raises ValueError."""
    # Arrange
    quiz = Quiz("Test Quiz")
    question = "What is the capital of France?"
    answers = ["London", "Paris", "Berlin", "Madrid"]
    
    # Act & Assert
    with pytest.raises(ValueError):
        quiz.add_question(question, answers, 4)  # Index out of range
    
    with pytest.raises(ValueError):
        quiz.add_question(question, answers, -1)  # Negative index


def test_get_question_count():
    """Test that get_question_count returns the correct number of questions."""
    # Arrange
    quiz = Quiz("Test Quiz")
    
    # Act & Assert
    assert quiz.get_question_count() == 0
    
    quiz.add_question("Question 1", ["A", "B"], 0)
    assert quiz.get_question_count() == 1
    
    quiz.add_question("Question 2", ["A", "B"], 0)
    assert quiz.get_question_count() == 2


def test_string_representation():
    """Test the string representation of a Quiz."""
    # Arrange
    quiz = Quiz("Test Quiz")
    
    # Act & Assert
    assert str(quiz) == "Quiz: Test Quiz (0 questions)"
    
    quiz.add_question("Question 1", ["A", "B"], 0)
    assert str(quiz) == "Quiz: Test Quiz (1 questions)"