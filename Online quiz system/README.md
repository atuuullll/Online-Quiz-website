# Online Quiz System

A modern, interactive quiz system built with HTML, CSS, JavaScript, and Flask.

## Features

- Modern and responsive UI
- Timer functionality
- Score tracking
- Navigation between questions
- Progress tracking
- Backend API for questions and scoring

## Project Structure

```
OnlineQuizSystem/
├── index.html      → Home Page (Start Quiz)
├── quiz.html       → Quiz Page (Questions, Timer, Score)
├── style.css       → Styling
├── script.js       → JavaScript (Quiz Logic)
├── server.py       → Python (Flask Backend)
├── assets/         → Images, Icons
└── README.md       → Project Documentation
```

## Setup Instructions

1. Install Python 3.x if not already installed
2. Install required Python packages:
   ```bash
   pip install flask flask-cors
   ```
3. Run the Flask server:
   ```bash
   python server.py
   ```
4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Click "Start Quiz" on the home page
2. Answer the questions within the time limit
3. Navigate between questions using Previous/Next buttons
4. Submit the quiz to see your score
5. Return to home page to start a new quiz

## Technologies Used

- HTML5
- CSS3
- JavaScript (ES6+)
- Python Flask
- Font Awesome Icons

## Contributing

Feel free to submit issues and enhancement requests! 