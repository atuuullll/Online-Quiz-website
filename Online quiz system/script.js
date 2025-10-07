// Quiz Configuration
const quizConfig = {
    totalQuestions: 5, // This will be updated based on available questions
    timeLimit: 30 * 60, // 30 minutes in seconds
    pointsPerQuestion: 10,
    warningTime: 5 * 60 // 5 minutes warning
};

// Fallback questions in case API fails
const fallbackQuestions = [
    {
        id: 1,
        question: "What is the capital of France?",
        options: ["London", "Berlin", "Paris", "Madrid"],
        correctAnswer: 2,
        explanation: "Paris is the capital and largest city of France."
    },
    {
        id: 2,
        question: "Which planet is known as the Red Planet?",
        options: ["Venus", "Mars", "Jupiter", "Saturn"],
        correctAnswer: 1,
        explanation: "Mars is called the Red Planet because of its reddish appearance."
    },
    {
        id: 3,
        question: "What is the largest mammal in the world?",
        options: ["African Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
        correctAnswer: 1,
        explanation: "The Blue Whale is the largest mammal, reaching lengths of up to 100 feet."
    },
    {
        id: 4,
        question: "Which element has the chemical symbol 'Au'?",
        options: ["Silver", "Copper", "Gold", "Aluminum"],
        correctAnswer: 2,
        explanation: "Au is the chemical symbol for Gold, derived from the Latin word 'Aurum'."
    },
    {
        id: 5,
        question: "What is the capital of Japan?",
        options: ["Seoul", "Beijing", "Tokyo", "Bangkok"],
        correctAnswer: 2,
        explanation: "Tokyo is the capital and largest city of Japan."
    }
];

// Quiz State
let currentQuestion = 0;
let score = 0;
let timeLeft = quizConfig.timeLimit;
let timer = null;
let userAnswers = [];  // Will be initialized based on number of questions
let isQuizSubmitted = false;
let playerName = '';
let startTime = null;
let quizQuestions = []; // Will hold the questions once loaded

// DOM Elements
const startQuizBtn = document.getElementById('startQuiz');
const timeLeftElement = document.getElementById('timeLeft');
const currentScoreElement = document.getElementById('currentScore');
const questionTextElement = document.getElementById('questionText');
const optionsContainer = document.getElementById('optionsContainer');
const prevQuestionBtn = document.getElementById('prevQuestion');
const nextQuestionBtn = document.getElementById('nextQuestion');
const submitQuizBtn = document.getElementById('submitQuiz');
const currentQuestionElement = document.getElementById('currentQuestion');
const totalQuestionsElement = document.getElementById('totalQuestions');

// Event Listeners
if (startQuizBtn) {
    startQuizBtn.addEventListener('click', startQuiz);
}

if (prevQuestionBtn) {
    prevQuestionBtn.addEventListener('click', () => navigateQuestion(-1));
}

if (nextQuestionBtn) {
    nextQuestionBtn.addEventListener('click', () => navigateQuestion(1));
}

if (submitQuizBtn) {
    submitQuizBtn.addEventListener('click', submitQuiz);
}

// Functions
function startQuiz() {
    // Get player name
    playerName = prompt('Please enter your name:', 'Anonymous');
    if (!playerName) playerName = 'Anonymous';
    
    // Reset quiz state
    currentQuestion = 0;
    score = 0;
    timeLeft = quizConfig.timeLimit;
    isQuizSubmitted = false;
    startTime = Date.now();
    
    // Save start time to localStorage
    localStorage.setItem('quizStartTime', startTime);
    localStorage.setItem('playerName', playerName);
    
    window.location.href = 'quiz.html';
}

function updateTimer() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    timeLeftElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    // Add warning class when time is running low
    if (timeLeft <= quizConfig.warningTime) {
        timeLeftElement.classList.add('warning');
    }
    
    if (timeLeft <= 0) {
        clearInterval(timer);
        submitQuiz();
    }
}

function startTimer() {
    // Check if there's a saved start time
    const savedStartTime = localStorage.getItem('quizStartTime');
    const savedPlayerName = localStorage.getItem('playerName');
    
    if (savedStartTime) {
        startTime = parseInt(savedStartTime);
        playerName = savedPlayerName || 'Anonymous';
        const elapsedTime = Math.floor((Date.now() - startTime) / 1000);
        timeLeft = Math.max(0, quizConfig.timeLimit - elapsedTime);
    }
    
    timer = setInterval(() => {
        timeLeft--;
        updateTimer();
    }, 1000);
}

async function loadQuestions() {
    try {
        console.log("Attempting to load questions from API...");
        
        // Get the API URL based on the current hostname
        const apiUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
            ? `http://${window.location.hostname}:5000/api/questions`
            : '/api/questions';
            
        console.log(`Fetching questions from: ${apiUrl}`);
        
        const response = await fetch(apiUrl);
        
        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (!data || !Array.isArray(data) || data.length === 0) {
            throw new Error('Invalid questions data received from server');
        }
        
        console.log(`Successfully loaded ${data.length} questions from API`);
        quizQuestions = data;
        
        // Update the total questions count based on actual available questions
        quizConfig.totalQuestions = Math.min(data.length, 10); // Use all questions up to 10 max
        console.log(`Quiz will use ${quizConfig.totalQuestions} questions`);
        
        // Initialize userAnswers array with the correct length
        userAnswers = new Array(quizConfig.totalQuestions).fill(null);
        
        return data;
    } catch (error) {
        console.error('Error loading questions from API:', error);
        console.log('Using fallback questions instead');
        quizQuestions = fallbackQuestions;
        quizConfig.totalQuestions = fallbackQuestions.length;
        userAnswers = new Array(quizConfig.totalQuestions).fill(null);
        return fallbackQuestions;
    }
}

async function displayQuestion() {
    if (currentQuestion >= quizConfig.totalQuestions) return;
    
    try {
        // Make sure questions are loaded
        if (quizQuestions.length === 0) {
            await loadQuestions();
        }
        
        const question = quizQuestions[currentQuestion];
        if (!question) {
            throw new Error(`Question at index ${currentQuestion} not found`);
        }
        
        questionTextElement.textContent = question.question;
        
        optionsContainer.innerHTML = '';
        question.options.forEach((option, index) => {
            const optionElement = document.createElement('div');
            optionElement.className = `option ${userAnswers[currentQuestion] === index ? 'selected' : ''}`;
            optionElement.textContent = option;
            
            // If quiz is submitted, show correct/incorrect answers
            if (isQuizSubmitted) {
                if (index === question.correctAnswer) {
                    optionElement.classList.add('correct');
                } else if (userAnswers[currentQuestion] === index) {
                    optionElement.classList.add('incorrect');
                }
                optionElement.disabled = true;
            } else {
                optionElement.addEventListener('click', () => selectOption(index));
            }
            
            optionsContainer.appendChild(optionElement);
        });
        
        updateNavigationButtons();
        currentQuestionElement.textContent = currentQuestion + 1;
        totalQuestionsElement.textContent = quizConfig.totalQuestions;
    } catch (error) {
        console.error('Error displaying question:', error);
        questionTextElement.textContent = "Error loading question. Please refresh the page or contact support.";
        optionsContainer.innerHTML = '<div class="error-message">There was a problem loading this question. Please try again.</div>';
    }
}

function selectOption(index) {
    userAnswers[currentQuestion] = index;
    displayQuestion();
}

function navigateQuestion(direction) {
    currentQuestion += direction;
    if (currentQuestion >= 0 && currentQuestion < quizConfig.totalQuestions) {
        displayQuestion();
    }
}

function updateNavigationButtons() {
    prevQuestionBtn.disabled = currentQuestion === 0;
    nextQuestionBtn.style.display = currentQuestion === quizConfig.totalQuestions - 1 ? 'none' : 'flex';
    submitQuizBtn.style.display = currentQuestion === quizConfig.totalQuestions - 1 ? 'flex' : 'none';
}

// Calculate the score from the user's answers
function calculateLocalScore() {
    let calculatedScore = 0;
    userAnswers.forEach((answer, index) => {
        if (index < quizQuestions.length && answer !== null && answer === quizQuestions[index].correctAnswer) {
            calculatedScore += quizConfig.pointsPerQuestion;
        }
    });
    return calculatedScore;
}

function showQuizResults(finalScore, message) {
    // Prepare result details
    const timeTaken = Math.floor((Date.now() - startTime) / 1000);
    const minutes = Math.floor(timeTaken / 60);
    const seconds = timeTaken % 60;
    const timeString = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    
    // Create a results container
    const resultsContainer = document.createElement('div');
    resultsContainer.className = 'quiz-results';
    resultsContainer.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 80%;
        max-width: 600px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        padding: 20px;
        z-index: 1000;
        max-height: 90vh;
        overflow-y: auto;
    `;
    
    // Create header
    const header = document.createElement('h2');
    header.textContent = 'Quiz Results';
    header.style.cssText = 'text-align: center; margin-bottom: 15px; color: #333;';
    resultsContainer.appendChild(header);
    
    // Score section
    const scoreSection = document.createElement('div');
    scoreSection.style.cssText = 'background: #f5f5f5; padding: 15px; border-radius: 6px; margin-bottom: 20px;';
    
    const playerInfo = document.createElement('p');
    playerInfo.innerHTML = `<strong>Player:</strong> ${playerName}`;
    playerInfo.style.margin = '5px 0';
    
    const scoreInfo = document.createElement('p');
    scoreInfo.innerHTML = `<strong>Score:</strong> ${finalScore}/${quizConfig.totalQuestions * quizConfig.pointsPerQuestion}`;
    scoreInfo.style.margin = '5px 0';
    
    const timeInfo = document.createElement('p');
    timeInfo.innerHTML = `<strong>Time taken:</strong> ${timeString}`;
    timeInfo.style.margin = '5px 0';
    
    scoreSection.appendChild(playerInfo);
    scoreSection.appendChild(scoreInfo);
    scoreSection.appendChild(timeInfo);
    resultsContainer.appendChild(scoreSection);
    
    // Question results
    if (quizQuestions.length > 0) {
        const questionsHeader = document.createElement('h3');
        questionsHeader.textContent = 'Question Results';
        questionsHeader.style.cssText = 'margin: 15px 0 10px; color: #444;';
        resultsContainer.appendChild(questionsHeader);
        
        userAnswers.forEach((answer, index) => {
            if (index >= quizQuestions.length) return;
            
            const question = quizQuestions[index];
            const isCorrect = answer === question.correctAnswer;
            
            const questionResult = document.createElement('div');
            questionResult.style.cssText = `
                margin-bottom: 12px;
                padding: 10px;
                border-radius: 6px;
                background: ${isCorrect ? '#e7f7e7' : '#ffebee'};
            `;
            
            const questionText = document.createElement('p');
            questionText.innerHTML = `<strong>Q${index + 1}:</strong> ${question.question}`;
            questionText.style.margin = '0 0 8px 0';
            
            const answerText = document.createElement('p');
            if (answer !== null) {
                answerText.innerHTML = `<strong>Your answer:</strong> ${question.options[answer]}`;
            } else {
                answerText.innerHTML = '<strong>Your answer:</strong> No answer';
            }
            answerText.style.margin = '4px 0';
            
            const correctText = document.createElement('p');
            correctText.innerHTML = `<strong>Correct answer:</strong> ${question.options[question.correctAnswer]}`;
            correctText.style.margin = '4px 0';
            
            const explanationText = document.createElement('p');
            explanationText.innerHTML = `<strong>Explanation:</strong> ${question.explanation || 'No explanation available'}`;
            explanationText.style.margin = '4px 0';
            
            questionResult.appendChild(questionText);
            questionResult.appendChild(answerText);
            questionResult.appendChild(correctText);
            questionResult.appendChild(explanationText);
            
            resultsContainer.appendChild(questionResult);
        });
    }
    
    // Add close button and home button
    const buttonContainer = document.createElement('div');
    buttonContainer.style.cssText = 'display: flex; justify-content: center; gap: 10px; margin-top: 20px;';
    
    const homeButton = document.createElement('button');
    homeButton.textContent = 'Go to Home';
    homeButton.style.cssText = `
        padding: 10px 20px;
        background: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
    `;
    homeButton.onclick = () => {
        document.body.removeChild(overlay);
        document.body.removeChild(resultsContainer);
        window.location.href = 'index.html';
    };
    
    const retryButton = document.createElement('button');
    retryButton.textContent = 'Take Quiz Again';
    retryButton.style.cssText = `
        padding: 10px 20px;
        background: #2196F3;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        font-weight: bold;
        transition: background-color 0.3s;
    `;
    retryButton.onmouseover = function() {
        this.style.backgroundColor = '#0b7dda';
    };
    retryButton.onmouseout = function() {
        this.style.backgroundColor = '#2196F3';
    };
    retryButton.onclick = function() {
        console.log("Try Again button clicked");
        const userConfirmed = confirm('Are you sure you want to take the quiz again?');
        console.log("User confirmation:", userConfirmed);
        
        if (userConfirmed) {
            console.log("User confirmed, reloading page");
            document.body.removeChild(overlay);
            document.body.removeChild(resultsContainer);
            window.location.reload();
        } else {
            console.log("User cancelled, staying on results page");
        }
    };
    
    buttonContainer.appendChild(homeButton);
    buttonContainer.appendChild(retryButton);
    resultsContainer.appendChild(buttonContainer);
    
    // Create overlay
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        z-index: 999;
    `;
    
    // Add to document
    document.body.appendChild(overlay);
    document.body.appendChild(resultsContainer);
    
    // Add click listener to overlay to close when clicked outside
    overlay.addEventListener('click', function(event) {
        // Only close if the click was directly on the overlay (not on its children)
        if (event.target === overlay) {
            // Ask for confirmation before closing
            if (confirm('Are you sure you want to close the results?')) {
                document.body.removeChild(overlay);
                document.body.removeChild(resultsContainer);
            }
        }
    });
}

async function submitQuiz() {
    if (isQuizSubmitted) return;
    
    clearInterval(timer);
    isQuizSubmitted = true;
    
    // Calculate time taken
    const timeTaken = Math.floor((Date.now() - startTime) / 1000);
    
    // Calculate score locally as backup
    const localScore = calculateLocalScore();
    
    // Update UI to show processing
    if (submitQuizBtn) {
        submitQuizBtn.disabled = true;
        submitQuizBtn.textContent = 'Processing...';
    }
    
    try {
        // Get the API URL based on the current hostname
        const apiUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
            ? `http://${window.location.hostname}:5000/api/submit-quiz`
            : '/api/submit-quiz';
            
        console.log(`Submitting quiz to: ${apiUrl}`);
        
        // Submit score to backend
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                playerName: playerName,
                answers: userAnswers,
                timeTaken: timeTaken
            })
        });
        
        let result;
        
        // Try to parse the response as JSON
        try {
            result = await response.json();
        } catch (parseError) {
            console.error('Error parsing JSON response:', parseError);
            // Use local score instead of throwing an error
            result = {
                score: localScore,
                total: quizConfig.totalQuestions * quizConfig.pointsPerQuestion
            };
        }
        
        // Check for errors in the response
        if (!response.ok) {
            console.warn('Server returned error, using local score instead');
            // Still show results but use local score
            result = {
                score: localScore,
                total: quizConfig.totalQuestions * quizConfig.pointsPerQuestion
            };
        }
        
        // Clear saved data
        localStorage.removeItem('quizStartTime');
        localStorage.removeItem('playerName');
        
        // Show results using server-provided score or local score if there was an error
        showQuizResults(result.score || localScore, result.message || 'Quiz submitted successfully!');
    } catch (error) {
        console.error('Error submitting quiz:', error);
        
        // Show results using local score calculation in case of error
        showQuizResults(localScore, 'An error occurred while submitting the quiz. Please try again later.');
    } finally {
        // Re-enable submit button
        if (submitQuizBtn) {
            submitQuizBtn.disabled = false;
            submitQuizBtn.textContent = 'Submit Quiz';
        }
    }
}

// Initialize quiz if on quiz page
if (window.location.pathname.includes('quiz.html')) {
    startTimer();
    loadQuestions().then(() => {
        displayQuestion();
    }).catch(error => {
        console.error('Failed to initialize quiz:', error);
        questionTextElement.textContent = "Error loading questions. Please refresh the page or contact support.";
    });
} 