"""
Quiz bot module.

This module defines the QuizBot class, which implements a chatbot that asks Python programming questions.
"""

from typing import List, Optional
from quizmaster.models.quiz import Quiz


class QuizBot:
    """
    A chatbot that asks Python programming questions and provides feedback on answers.
    
    Attributes:
        quiz (Quiz): The quiz containing the questions to ask.
        current_question_index (int): The index of the current question being asked.
    """
    
    def __init__(self, quiz: Optional[Quiz] = None):
        """
        Initialize a new QuizBot.
        
        Args:
            quiz: An optional Quiz object. If not provided, a default quiz with Python questions will be created.
        """
        if quiz is None:
            quiz = self._create_default_quiz()
        self.quiz = quiz
        self.current_question_index = 0
    
    def _create_default_quiz(self) -> Quiz:
        """
        Create a default quiz with Python programming questions.
        
        Returns:
            A Quiz object with default Python questions.
        """
        quiz = Quiz("Python Programming Quiz", "Test your knowledge of Python programming basics")
        
        # Question 1
        quiz.add_question(
            "What is the correct way to create a variable named 'age' with the value 25?",
            [
                "variable age = 25",
                "age = 25",
                "int age = 25",
                "age := 25"
            ],
            1  # Correct answer is "age = 25"
        )
        
        # Question 2
        quiz.add_question(
            "Which of the following is a valid way to comment in Python?",
            [
                "// This is a comment",
                "/* This is a comment */",
                "# This is a comment",
                "<!-- This is a comment -->"
            ],
            2  # Correct answer is "# This is a comment"
        )
        
        # Question 3
        quiz.add_question(
            "What does the len() function do in Python?",
            [
                "Returns the largest item in an iterable",
                "Returns the length of an object",
                "Returns the lowest item in an iterable",
                "Returns the last item in an iterable"
            ],
            1  # Correct answer is "Returns the length of an object"
        )
        
        # Question 4
        quiz.add_question(
            "Which of the following is NOT a built-in data type in Python?",
            [
                "list",
                "dictionary",
                "array",
                "tuple"
            ],
            2  # Correct answer is "array"
        )
        
        # Question 5
        quiz.add_question(
            "What is the output of print(2 ** 3)?",
            [
                "6",
                "8",
                "5",
                "Error"
            ],
            1  # Correct answer is "8"
        )
        
        return quiz
    
    def start(self) -> None:
        """
        Start the quiz bot interaction loop.
        
        This method runs a continuous loop that:
        1. Displays the current question and answer choices
        2. Accepts user input
        3. Provides feedback on whether the answer is correct
        4. Allows the user to quit the chat
        """
        print(f"Welcome to the {self.quiz.title}!")
        print(f"{self.quiz.description}\n")
        print("For each question, enter the number of your answer or 'q' to quit.")
        
        while self.current_question_index < self.quiz.get_question_count():
            question_data = self.quiz.questions[self.current_question_index]
            
            # Display the question
            print(f"\nQuestion {self.current_question_index + 1}: {question_data['question']}")
            
            # Display the answer choices
            for i, answer in enumerate(question_data['answers']):
                print(f"{i + 1}. {answer}")
            
            # Get user input
            user_input = input("\nYour answer (or 'q' to quit): ").strip().lower()
            
            # Check if user wants to quit
            if user_input == 'q':
                print("Thanks for playing!")
                return
            
            # Validate and process the answer
            try:
                user_answer_index = int(user_input) - 1  # Convert to 0-based index
                
                if 0 <= user_answer_index < len(question_data['answers']):
                    # Check if the answer is correct
                    if user_answer_index == question_data['correct_answer_index']:
                        print("Correct! Well done!")
                    else:
                        correct_answer = question_data['answers'][question_data['correct_answer_index']]
                        print(f"Sorry, that's incorrect. The correct answer is: {correct_answer}")
                    
                    # Move to the next question
                    self.current_question_index += 1
                else:
                    print(f"Please enter a number between 1 and {len(question_data['answers'])}")
            except ValueError:
                print("Please enter a valid number or 'q' to quit")
        
        # Quiz completed
        print("\nCongratulations! You've completed the quiz.")
        print("Thanks for playing!")


def main():
    """
    Main function to run the quiz bot.
    """
    bot = QuizBot()
    bot.start()


if __name__ == "__main__":
    main()