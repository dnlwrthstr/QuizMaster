# Fix Question Text Display Issue

## Issue Description
The question text was not displaying correctly on the quiz page due to a mismatch between the HTML element ID and the JavaScript code that references it.

## Changes Made
1. In `frontend/index.html`:
   - Changed the ID of the question text element from `question-text` to `quiz-question-text` on line 96

2. In `frontend/script.js`:
   - Updated references to `question-text` to use `quiz-question-text` in the `showQuestion` function (lines 295 and 297)

## Testing
The changes were tested by:
1. Running the application
2. Creating a quiz with questions
3. Starting the quiz
4. Verifying that question text displays correctly on the quiz page

## Impact
This fix ensures that question text is properly displayed when users take quizzes, improving the overall user experience.