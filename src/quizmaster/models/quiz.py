"""
Quiz model module.

This module defines the Quiz class, which represents a quiz in the QuizMaster application.
"""

from typing import List, Optional


class Quiz:
    """
    Represents a quiz with questions and answers.
    
    Attributes:
        title (str): The title of the quiz.
        description (str): A description of the quiz.
        questions (List[dict]): A list of questions, each with answers and correct answer.
    """
    
    def __init__(self, title: str, description: Optional[str] = None):
        """
        Initialize a new Quiz.
        
        Args:
            title: The title of the quiz.
            description: An optional description of the quiz.
        """
        self.title = title
        self.description = description or ""
        self.questions: List[dict] = []
    
    def add_question(self, question: str, answers: List[str], correct_answer_index: int) -> None:
        """
        Add a question to the quiz.
        
        Args:
            question: The question text.
            answers: A list of possible answers.
            correct_answer_index: The index of the correct answer in the answers list.
        
        Raises:
            ValueError: If correct_answer_index is out of range.
        """
        if not 0 <= correct_answer_index < len(answers):
            raise ValueError("Correct answer index out of range")
        
        self.questions.append({
            "question": question,
            "answers": answers,
            "correct_answer_index": correct_answer_index
        })
    
    def get_question_count(self) -> int:
        """
        Get the number of questions in the quiz.
        
        Returns:
            The number of questions.
        """
        return len(self.questions)
    
    def __str__(self) -> str:
        """
        Return a string representation of the quiz.
        
        Returns:
            A string representation.
        """
        return f"Quiz: {self.title} ({self.get_question_count()} questions)"