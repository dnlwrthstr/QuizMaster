"""
Main module for the QuizMaster application.

This module provides the entry point for running the QuizMaster application
and defines the FastAPI REST endpoints.
"""

from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import uvicorn
import os

from quizmaster.services.quiz_bot import QuizBot
from quizmaster.models.quiz import Quiz


# Pydantic models for API
class AnswerModel(BaseModel):
    text: str
    is_correct: bool = False


class QuestionModel(BaseModel):
    id: int
    text: str
    answers: List[AnswerModel]


class QuestionCreateModel(BaseModel):
    text: str
    answers: List[str]
    correct_answer_index: int


class QuizModel(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    questions: Optional[List[QuestionModel]] = None


class QuizCreateModel(BaseModel):
    title: str
    description: Optional[str] = None


class AnswerSubmissionModel(BaseModel):
    answer_index: int


class AnswerResponseModel(BaseModel):
    is_correct: bool
    correct_answer: Optional[str] = None
    message: str


# Create FastAPI app
app = FastAPI(
    title="QuizMaster API",
    description="REST API for the QuizMaster application",
    version="1.0.0"
)

# Mount static files directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Add a route for favicon.ico
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = os.path.join(static_dir, "favicon.ico")
    return FileResponse(favicon_path)

# In-memory storage for quizzes
quizzes = {}
quiz_id_counter = 0


# Helper function to convert Quiz to QuizModel
def quiz_to_model(quiz: Quiz, quiz_id: int) -> QuizModel:
    questions = []
    for i, q in enumerate(quiz.questions):
        answers = []
        for j, a in enumerate(q["answers"]):
            answers.append(AnswerModel(
                text=a,
                is_correct=(j == q["correct_answer_index"])
            ))
        questions.append(QuestionModel(
            id=i,
            text=q["question"],
            answers=answers
        ))

    return QuizModel(
        id=quiz_id,
        title=quiz.title,
        description=quiz.description,
        questions=questions
    )


# API Routes
@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to QuizMaster API!"}


@app.get("/quizzes", response_model=List[QuizModel])
async def get_quizzes():
    """Get all quizzes."""
    return [quiz_to_model(quiz, quiz_id) for quiz_id, quiz in quizzes.items()]


@app.post("/quizzes", response_model=QuizModel, status_code=status.HTTP_201_CREATED)
async def create_quiz(quiz_data: QuizCreateModel):
    """Create a new quiz."""
    global quiz_id_counter

    quiz = Quiz(title=quiz_data.title, description=quiz_data.description)
    quiz_id = quiz_id_counter
    quiz_id_counter += 1

    quizzes[quiz_id] = quiz
    return quiz_to_model(quiz, quiz_id)


@app.get("/quizzes/{quiz_id}", response_model=QuizModel)
async def get_quiz(quiz_id: int):
    """Get a specific quiz by ID."""
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return quiz_to_model(quizzes[quiz_id], quiz_id)


@app.post("/quizzes/{quiz_id}/questions", response_model=QuizModel)
async def add_question(quiz_id: int, question_data: QuestionCreateModel):
    """Add a question to a quiz."""
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz = quizzes[quiz_id]
    try:
        quiz.add_question(
            question=question_data.text,
            answers=question_data.answers,
            correct_answer_index=question_data.correct_answer_index
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return quiz_to_model(quiz, quiz_id)


@app.get("/quizzes/{quiz_id}/questions/{question_id}", response_model=QuestionModel)
async def get_question(quiz_id: int, question_id: int):
    """Get a specific question from a quiz."""
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz = quizzes[quiz_id]
    if question_id < 0 or question_id >= quiz.get_question_count():
        raise HTTPException(status_code=404, detail="Question not found")

    question_data = quiz.questions[question_id]
    answers = []
    for i, answer in enumerate(question_data["answers"]):
        answers.append(AnswerModel(
            text=answer,
            is_correct=(i == question_data["correct_answer_index"])
        ))

    return QuestionModel(
        id=question_id,
        text=question_data["question"],
        answers=answers
    )


@app.post("/quizzes/{quiz_id}/questions/{question_id}/submit", response_model=AnswerResponseModel)
async def submit_answer(quiz_id: int, question_id: int, submission: AnswerSubmissionModel):
    """Submit an answer to a question."""
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz = quizzes[quiz_id]
    if question_id < 0 or question_id >= quiz.get_question_count():
        raise HTTPException(status_code=404, detail="Question not found")

    question_data = quiz.questions[question_id]
    if submission.answer_index < 0 or submission.answer_index >= len(question_data["answers"]):
        raise HTTPException(status_code=400, detail="Invalid answer index")

    is_correct = submission.answer_index == question_data["correct_answer_index"]
    correct_answer = question_data["answers"][question_data["correct_answer_index"]]

    if is_correct:
        message = "Correct! Well done!"
        return AnswerResponseModel(is_correct=True, message=message)
    else:
        message = f"Sorry, that's incorrect."
        return AnswerResponseModel(
            is_correct=False,
            correct_answer=correct_answer,
            message=message
        )


@app.post("/init-default-quiz", response_model=QuizModel)
async def init_default_quiz():
    """Initialize the default Python quiz."""
    global quiz_id_counter

    bot = QuizBot()
    quiz_id = quiz_id_counter
    quiz_id_counter += 1

    quizzes[quiz_id] = bot.quiz
    return quiz_to_model(bot.quiz, quiz_id)


def main():
    """
    Main function to run the QuizMaster application.

    This function starts the FastAPI application using Uvicorn.
    """
    uvicorn.run("quizmaster.main:app", host="0.0.0.0", port=8090, reload=True)


if __name__ == "__main__":
    main()
