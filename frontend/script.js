// Global variables
let currentQuizId = null;
let currentQuestionIndex = 0;
let quizQuestions = [];
let userScore = 0;

// API URL (assuming the backend is running on the same host)
const API_BASE_URL = 'http://localhost:8091';

// DOM Elements
const homeLink = document.getElementById('home-link');
const createQuizLink = document.getElementById('create-quiz-link');
const initDefaultQuizBtn = document.getElementById('init-default-quiz');
const quizListSection = document.getElementById('quiz-list-section');
const createQuizSection = document.getElementById('create-quiz-section');
const quizDetailSection = document.getElementById('quiz-detail-section');
const addQuestionSection = document.getElementById('add-question-section');
const takeQuizSection = document.getElementById('take-quiz-section');
const quizList = document.getElementById('quiz-list');
const createQuizForm = document.getElementById('create-quiz-form');
const addQuestionForm = document.getElementById('add-question-form');
const addQuestionBtn = document.getElementById('add-question-btn');
const startQuizBtn = document.getElementById('start-quiz-btn');
const addAnswerBtn = document.getElementById('add-answer-btn');
const nextQuestionBtn = document.getElementById('next-question-btn');
const returnToQuizzesBtn = document.getElementById('return-to-quizzes-btn');

// Navigation functions
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.page').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show the selected section
    document.getElementById(sectionId).classList.add('active');
    
    // Update navigation active state
    document.querySelectorAll('nav a').forEach(link => {
        link.classList.remove('active');
    });
    
    if (sectionId === 'quiz-list-section') {
        homeLink.classList.add('active');
    } else if (sectionId === 'create-quiz-section') {
        createQuizLink.classList.add('active');
    }
}

// API functions
async function fetchQuizzes() {
    try {
        const response = await fetch(`${API_BASE_URL}/quizzes`);
        if (!response.ok) {
            throw new Error('Failed to fetch quizzes');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching quizzes:', error);
        return [];
    }
}

async function fetchQuiz(quizId) {
    try {
        const response = await fetch(`${API_BASE_URL}/quizzes/${quizId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch quiz');
        }
        return await response.json();
    } catch (error) {
        console.error(`Error fetching quiz ${quizId}:`, error);
        return null;
    }
}

async function createQuiz(quizData) {
    try {
        const response = await fetch(`${API_BASE_URL}/quizzes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(quizData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to create quiz');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error creating quiz:', error);
        return null;
    }
}

async function addQuestion(quizId, questionData) {
    try {
        const response = await fetch(`${API_BASE_URL}/quizzes/${quizId}/questions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(questionData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to add question');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error adding question:', error);
        return null;
    }
}

async function submitAnswer(quizId, questionId, answerIndex) {
    try {
        const response = await fetch(`${API_BASE_URL}/quizzes/${quizId}/questions/${questionId}/submit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ answer_index: answerIndex })
        });
        
        if (!response.ok) {
            throw new Error('Failed to submit answer');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error submitting answer:', error);
        return null;
    }
}

async function initDefaultQuiz() {
    try {
        const response = await fetch(`${API_BASE_URL}/init-default-quiz`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error('Failed to initialize default quiz');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error initializing default quiz:', error);
        return null;
    }
}

// UI functions
function renderQuizList(quizzes) {
    quizList.innerHTML = '';
    
    if (quizzes.length === 0) {
        quizList.innerHTML = '<div class="loading">No quizzes available. Create a new quiz or initialize the default quiz.</div>';
        return;
    }
    
    quizzes.forEach(quiz => {
        const quizCard = document.createElement('div');
        quizCard.className = 'card';
        quizCard.innerHTML = `
            <h3>${quiz.title}</h3>
            <p>${quiz.description || 'No description'}</p>
            <p>Questions: ${quiz.questions ? quiz.questions.length : 0}</p>
            <button class="btn primary view-quiz-btn" data-quiz-id="${quiz.id}">View Quiz</button>
        `;
        quizList.appendChild(quizCard);
    });
    
    // Add event listeners to view quiz buttons
    document.querySelectorAll('.view-quiz-btn').forEach(button => {
        button.addEventListener('click', async () => {
            const quizId = parseInt(button.getAttribute('data-quiz-id'));
            await loadQuizDetail(quizId);
        });
    });
}

async function loadQuizDetail(quizId) {
    const quiz = await fetchQuiz(quizId);
    if (!quiz) return;
    
    currentQuizId = quizId;
    
    // Update quiz detail section
    document.getElementById('quiz-detail-title').textContent = quiz.title;
    document.getElementById('quiz-detail-description').textContent = quiz.description || 'No description';
    
    // Render questions
    const questionList = document.getElementById('question-list');
    questionList.innerHTML = '';
    
    if (!quiz.questions || quiz.questions.length === 0) {
        questionList.innerHTML = '<div class="loading">No questions available. Add some questions to this quiz.</div>';
        startQuizBtn.disabled = true;
    } else {
        quiz.questions.forEach(question => {
            const questionItem = document.createElement('div');
            questionItem.className = 'question-item';
            questionItem.innerHTML = `
                <h3>${question.text}</h3>
                <p>Answers: ${question.answers.length}</p>
            `;
            questionList.appendChild(questionItem);
        });
        startQuizBtn.disabled = false;
    }
    
    // Show quiz detail section
    showSection('quiz-detail-section');
}

function setupAddQuestionForm() {
    // Reset form
    addQuestionForm.reset();
    
    // Reset answers container (keep only 2 default answers)
    const answersContainer = document.getElementById('answers-container');
    answersContainer.innerHTML = `
        <div class="form-group answer-group">
            <label>Answer 1</label>
            <input type="text" name="answers[]" required>
            <input type="radio" name="correct_answer" value="0" checked> Correct
        </div>
        <div class="form-group answer-group">
            <label>Answer 2</label>
            <input type="text" name="answers[]" required>
            <input type="radio" name="correct_answer" value="1"> Correct
        </div>
    `;
    
    // Show add question section
    showSection('add-question-section');
}

function addAnswerField() {
    const answersContainer = document.getElementById('answers-container');
    const answerCount = answersContainer.children.length;
    
    const answerGroup = document.createElement('div');
    answerGroup.className = 'form-group answer-group';
    answerGroup.innerHTML = `
        <label>Answer ${answerCount + 1}</label>
        <input type="text" name="answers[]" required>
        <input type="radio" name="correct_answer" value="${answerCount}"> Correct
    `;
    
    answersContainer.appendChild(answerGroup);
}

async function startQuiz() {
    const quiz = await fetchQuiz(currentQuizId);
    if (!quiz || !quiz.questions || quiz.questions.length === 0) return;
    
    // Reset quiz state
    currentQuestionIndex = 0;
    userScore = 0;
    quizQuestions = quiz.questions;
    
    // Update quiz title
    document.getElementById('take-quiz-title').textContent = quiz.title;
    
    // Update progress
    document.getElementById('current-question').textContent = '1';
    document.getElementById('total-questions').textContent = quizQuestions.length;
    
    // Hide feedback and completion sections
    document.getElementById('feedback-container').classList.add('hidden');
    document.getElementById('quiz-complete').classList.add('hidden');
    
    // Show the first question
    showQuestion(currentQuestionIndex);
    
    // Show take quiz section
    showSection('take-quiz-section');
}

function showQuestion(index) {
    const question = quizQuestions[index];
    
    // Update question text
    document.getElementById('question-text').textContent = question.text;
    
    // Render answer options
    const answersList = document.getElementById('answers-list');
    answersList.innerHTML = '';
    
    question.answers.forEach((answer, i) => {
        const answerButton = document.createElement('button');
        answerButton.className = 'answer-option';
        answerButton.textContent = answer.text;
        answerButton.setAttribute('data-index', i);
        answerButton.addEventListener('click', () => selectAnswer(i));
        answersList.appendChild(answerButton);
    });
}

async function selectAnswer(answerIndex) {
    // Disable all answer buttons
    document.querySelectorAll('.answer-option').forEach(button => {
        button.disabled = true;
    });
    
    // Highlight selected answer
    const selectedButton = document.querySelector(`.answer-option[data-index="${answerIndex}"]`);
    selectedButton.classList.add('selected');
    
    // Submit answer to API
    const result = await submitAnswer(currentQuizId, currentQuestionIndex, answerIndex);
    
    if (result) {
        // Update score if correct
        if (result.is_correct) {
            userScore++;
            selectedButton.classList.add('correct');
        } else {
            selectedButton.classList.add('incorrect');
            
            // Highlight correct answer if available
            if (result.correct_answer) {
                const correctAnswerIndex = quizQuestions[currentQuestionIndex].answers
                    .findIndex(answer => answer.is_correct);
                
                if (correctAnswerIndex >= 0) {
                    const correctButton = document.querySelector(`.answer-option[data-index="${correctAnswerIndex}"]`);
                    correctButton.classList.add('correct');
                }
            }
        }
        
        // Show feedback
        const feedbackContainer = document.getElementById('feedback-container');
        const feedbackMessage = document.getElementById('feedback-message');
        feedbackMessage.textContent = result.message;
        feedbackContainer.classList.remove('hidden');
        
        // Check if this is the last question
        if (currentQuestionIndex === quizQuestions.length - 1) {
            // Show completion message instead of next button
            document.getElementById('next-question-btn').classList.add('hidden');
            document.getElementById('final-score').textContent = userScore;
            document.getElementById('total-score').textContent = quizQuestions.length;
            document.getElementById('quiz-complete').classList.remove('hidden');
        } else {
            document.getElementById('next-question-btn').classList.remove('hidden');
        }
    }
}

function nextQuestion() {
    currentQuestionIndex++;
    
    // Update progress
    document.getElementById('current-question').textContent = currentQuestionIndex + 1;
    
    // Hide feedback
    document.getElementById('feedback-container').classList.add('hidden');
    
    // Show next question
    showQuestion(currentQuestionIndex);
}

// Event listeners
document.addEventListener('DOMContentLoaded', async () => {
    // Navigation
    homeLink.addEventListener('click', (e) => {
        e.preventDefault();
        loadQuizzes();
    });
    
    createQuizLink.addEventListener('click', (e) => {
        e.preventDefault();
        showSection('create-quiz-section');
    });
    
    // Initialize default quiz
    initDefaultQuizBtn.addEventListener('click', async () => {
        const quiz = await initDefaultQuiz();
        if (quiz) {
            await loadQuizzes();
        }
    });
    
    // Create quiz form
    createQuizForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const quizData = {
            title: document.getElementById('quiz-title').value,
            description: document.getElementById('quiz-description').value
        };
        
        const quiz = await createQuiz(quizData);
        if (quiz) {
            currentQuizId = quiz.id;
            await loadQuizDetail(quiz.id);
        }
    });
    
    // Add question button
    addQuestionBtn.addEventListener('click', () => {
        setupAddQuestionForm();
    });
    
    // Add answer button
    addAnswerBtn.addEventListener('click', () => {
        addAnswerField();
    });
    
    // Add question form
    addQuestionForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const questionText = document.getElementById('question-text').value;
        const answerInputs = document.querySelectorAll('input[name="answers[]"]');
        const correctAnswerIndex = parseInt(document.querySelector('input[name="correct_answer"]:checked').value);
        
        const answers = Array.from(answerInputs).map(input => input.value);
        
        const questionData = {
            text: questionText,
            answers: answers,
            correct_answer_index: correctAnswerIndex
        };
        
        const quiz = await addQuestion(currentQuizId, questionData);
        if (quiz) {
            await loadQuizDetail(currentQuizId);
        }
    });
    
    // Start quiz button
    startQuizBtn.addEventListener('click', () => {
        startQuiz();
    });
    
    // Next question button
    nextQuestionBtn.addEventListener('click', () => {
        nextQuestion();
    });
    
    // Return to quizzes button
    returnToQuizzesBtn.addEventListener('click', () => {
        loadQuizzes();
    });
    
    // Load quizzes on initial page load
    await loadQuizzes();
});

// Helper function to load quizzes
async function loadQuizzes() {
    quizList.innerHTML = '<div class="loading">Loading quizzes...</div>';
    const quizzes = await fetchQuizzes();
    renderQuizList(quizzes);
    showSection('quiz-list-section');
}