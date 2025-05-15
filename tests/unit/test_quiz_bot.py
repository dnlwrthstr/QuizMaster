"""
Unit tests for the QuizBot class.
"""

import pytest
from unittest.mock import patch

from quizmaster.models.quiz import Quiz
from quizmaster.services.quiz_bot import QuizBot


def test_quiz_bot_initialization():
    """Test that a QuizBot can be initialized with a default quiz."""
    # Arrange & Act
    bot = QuizBot()
    
    # Assert
    assert bot.quiz is not None
    assert bot.quiz.title == "Python Programming Quiz"
    assert bot.current_question_index == 0
    assert bot.quiz.get_question_count() == 5  # We added 5 default questions


def test_quiz_bot_initialization_with_custom_quiz():
    """Test that a QuizBot can be initialized with a custom quiz."""
    # Arrange
    custom_quiz = Quiz("Custom Quiz", "A custom quiz for testing")
    custom_quiz.add_question("Test question?", ["A", "B", "C"], 0)
    
    # Act
    bot = QuizBot(custom_quiz)
    
    # Assert
    assert bot.quiz is custom_quiz
    assert bot.quiz.title == "Custom Quiz"
    assert bot.current_question_index == 0
    assert bot.quiz.get_question_count() == 1


@patch('builtins.input', side_effect=['1', 'q'])
@patch('builtins.print')
def test_quiz_bot_correct_answer(mock_print, mock_input):
    """Test that the QuizBot correctly handles a correct answer."""
    # Arrange
    quiz = Quiz("Test Quiz")
    quiz.add_question("Test question?", ["Correct", "Wrong"], 0)
    bot = QuizBot(quiz)
    
    # Act
    bot.start()
    
    # Assert
    # Check that "Correct!" was printed
    assert any("Correct!" in str(call) for call in mock_print.call_args_list)


@patch('builtins.input', side_effect=['2', 'q'])
@patch('builtins.print')
def test_quiz_bot_incorrect_answer(mock_print, mock_input):
    """Test that the QuizBot correctly handles an incorrect answer."""
    # Arrange
    quiz = Quiz("Test Quiz")
    quiz.add_question("Test question?", ["Correct", "Wrong"], 0)
    bot = QuizBot(quiz)
    
    # Act
    bot.start()
    
    # Assert
    # Check that "incorrect" was printed
    assert any("incorrect" in str(call).lower() for call in mock_print.call_args_list)
    # Check that the correct answer was shown
    assert any("Correct" in str(call) for call in mock_print.call_args_list)


@patch('builtins.input', side_effect=['q'])
@patch('builtins.print')
def test_quiz_bot_quit(mock_print, mock_input):
    """Test that the QuizBot correctly handles quitting."""
    # Arrange
    bot = QuizBot()
    
    # Act
    bot.start()
    
    # Assert
    # Check that "Thanks for playing" was printed
    assert any("Thanks for playing" in str(call) for call in mock_print.call_args_list)


@patch('builtins.input', side_effect=['invalid', '1', 'q'])
@patch('builtins.print')
def test_quiz_bot_invalid_input(mock_print, mock_input):
    """Test that the QuizBot correctly handles invalid input."""
    # Arrange
    quiz = Quiz("Test Quiz")
    quiz.add_question("Test question?", ["Correct", "Wrong"], 0)
    bot = QuizBot(quiz)
    
    # Act
    bot.start()
    
    # Assert
    # Check that an error message was printed
    assert any("valid number" in str(call).lower() for call in mock_print.call_args_list)