"""
Main module for the QuizMaster application.

This module provides the entry point for running the QuizMaster application.
"""

from quizmaster.services.quiz_bot import QuizBot


def main():
    """
    Main function to run the QuizMaster application.
    
    This function creates a QuizBot instance and starts the interactive quiz.
    """
    print("Welcome to QuizMaster!")
    print("======================\n")
    
    # Create and start the quiz bot
    bot = QuizBot()
    bot.start()


if __name__ == "__main__":
    main()