from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime
import os
import sqlite3  # Fallback to SQLite if MySQL fails

# Try to import MySQL connector, but handle if it's not available
try:
    import mysql.connector
    from mysql.connector import Error
    MYSQL_AVAILABLE = True
except ImportError:
    print("MySQL connector not available. Will use SQLite as fallback.")
    MYSQL_AVAILABLE = False

# Initialize Flask app
app = Flask(__name__, static_folder='.')
CORS(app)

# For debugging
app.config['DEBUG'] = True

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',     # Change to your MySQL username
    'password': '',     # Change to your MySQL password
    'database': 'quiz_system'
}

# Fallback SQLite database
SQLITE_DB = 'quiz.db'

# Quiz questions
QUESTIONS = [
    {
        "id": 1,
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correctAnswer": 2,
        "explanation": "Paris is the capital and largest city of France."
    },
    {
        "id": 2,
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correctAnswer": 1,
        "explanation": "Mars is called the Red Planet because of its reddish appearance."
    },
    {
        "id": 3,
        "question": "What is the largest mammal in the world?",
        "options": ["African Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
        "correctAnswer": 1,
        "explanation": "The Blue Whale is the largest mammal, reaching lengths of up to 100 feet."
    },
    {
        "id": 4,
        "question": "Which element has the chemical symbol 'Au'?",
        "options": ["Silver", "Copper", "Gold", "Aluminum"],
        "correctAnswer": 2,
        "explanation": "Au is the chemical symbol for Gold, derived from the Latin word 'Aurum'."
    },
    {
        "id": 5,
        "question": "What is the capital of Japan?",
        "options": ["Seoul", "Beijing", "Tokyo", "Bangkok"],
        "correctAnswer": 2,
        "explanation": "Tokyo is the capital and largest city of Japan."
    }
]

# Make sure QUESTIONS is always initialized with at least some questions
if not QUESTIONS:
    QUESTIONS = [
        {
            "id": 1,
            "question": "What is the capital of France?",
            "options": ["London", "Berlin", "Paris", "Madrid"],
            "correctAnswer": 2,
            "explanation": "Paris is the capital and largest city of France."
        },
        {
            "id": 2,
            "question": "Which planet is known as the Red Planet?",
            "options": ["Venus", "Mars", "Jupiter", "Saturn"],
            "correctAnswer": 1,
            "explanation": "Mars is called the Red Planet because of its reddish appearance."
        }
    ]

# Track whether we're using MySQL or SQLite
using_mysql = False

# Since file storage is troublesome, let's add a memory-only mode
MEMORY_ONLY_MODE = True

def get_db_connection():
    """Create a database connection to either MySQL or SQLite."""
    global using_mysql
    
    # Try MySQL first if available
    if MYSQL_AVAILABLE:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            using_mysql = True
            return conn
        except Exception as e:
            print(f"Error connecting to MySQL: {e}")
            print("Falling back to SQLite...")
    
    # Fall back to SQLite
    try:
        conn = sqlite3.connect(SQLITE_DB)
        conn.row_factory = sqlite3.Row
        using_mysql = False
        return conn
    except Exception as e:
        print(f"Error connecting to SQLite: {e}")
        return None

def init_db():
    """Initialize the database with required tables."""
    global using_mysql
    
    # Try to initialize MySQL first if available
    if MYSQL_AVAILABLE:
        try:
            # Create MySQL database if it doesn't exist
            conn = mysql.connector.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
            cursor = conn.cursor()
            
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            conn.commit()
            conn.close()
            
            # Connect to the database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Create quiz_scores table in MySQL
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quiz_scores (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    player_name VARCHAR(100) NOT NULL,
                    score INT NOT NULL,
                    total_questions INT NOT NULL,
                    time_taken INT NOT NULL,
                    date_taken DATETIME NOT NULL,
                    answers JSON NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            print("MySQL database initialized successfully")
            using_mysql = True
            return True
        except Exception as e:
            print(f"Error initializing MySQL: {e}")
            print("Falling back to SQLite...")
    
    # Fall back to SQLite
    try:
        conn = sqlite3.connect(SQLITE_DB)
        cursor = conn.cursor()
        
        # Create quiz_scores table in SQLite
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                time_taken INTEGER NOT NULL,
                date_taken TEXT NOT NULL,
                answers TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print("SQLite database initialized successfully")
        using_mysql = False
        return True
    except Exception as e:
        print(f"Error initializing SQLite: {e}")
        return False

def calculate_score(answers):
    """Calculate the quiz score based on answers."""
    score = 0
    for i, answer in enumerate(answers):
        if i < len(QUESTIONS) and answer is not None and answer == QUESTIONS[i]['correctAnswer']:
            score += 10
    return score

# Initialize database on startup
db_initialized = init_db()
if not db_initialized:
    print("WARNING: Database initialization failed. Using in-memory storage as fallback.")
    # Create in-memory storage for scores as last resort
    in_memory_scores = []

@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Get all quiz questions."""
    try:
        # Load questions from file if not already loaded
        global QUESTIONS
        
        if not QUESTIONS or len(QUESTIONS) == 0:
            load_questions_from_file()
            
        # Make sure we always have at least the default questions
        if not QUESTIONS or len(QUESTIONS) == 0:
            # Default questions as fallback
            QUESTIONS = [
                {
                    "id": 1,
                    "question": "What is the capital of France?",
                    "options": ["London", "Berlin", "Paris", "Madrid"],
                    "correctAnswer": 2,
                    "explanation": "Paris is the capital and largest city of France."
                },
                {
                    "id": 2,
                    "question": "Which planet is known as the Red Planet?",
                    "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                    "correctAnswer": 1,
                    "explanation": "Mars is called the Red Planet because of its reddish appearance."
                }
            ]
        
        return jsonify(QUESTIONS)
    except Exception as e:
        print(f"Error getting questions: {e}")
        # Return the error but also provide default questions
        return jsonify([
            {
                "id": 1,
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correctAnswer": 2,
                "explanation": "Paris is the capital and largest city of France."
            },
            {
                "id": 2,
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "correctAnswer": 1,
                "explanation": "Mars is called the Red Planet because of its reddish appearance."
            }
        ]), 200  # Still return 200 so the frontend doesn't break

@app.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    """Handle quiz submission and score storage."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400

        # Extract data from request
        player_name = data.get('playerName', 'Anonymous')
        answers = data.get('answers', [])
        time_taken = data.get('timeTaken', 0)
        
        # Validate answers
        if len(answers) != len(QUESTIONS):
            return jsonify({
                'error': f'Invalid number of answers. Expected {len(QUESTIONS)}, got {len(answers)}'
            }), 400
        
        # Calculate score
        score = calculate_score(answers)
        
        # Try to store in database
        success = False
        
        if db_initialized:
            try:
                conn = get_db_connection()
                if conn:
                    cursor = conn.cursor()
                    
                    # Different syntax for MySQL vs SQLite
                    if using_mysql:
                        query = '''
                            INSERT INTO quiz_scores 
                            (player_name, score, total_questions, time_taken, date_taken, answers)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        '''
                    else:
                        query = '''
                            INSERT INTO quiz_scores 
                            (player_name, score, total_questions, time_taken, date_taken, answers)
                            VALUES (?, ?, ?, ?, ?, ?)
                        '''
                    
                    current_time = datetime.now().isoformat()
                    
                    cursor.execute(query, (
                        player_name,
                        score,
                        len(QUESTIONS),
                        time_taken,
                        current_time if not using_mysql else datetime.now(),
                        json.dumps(answers)
                    ))
                    
                    conn.commit()
                    conn.close()
                    success = True
                    print(f"Score saved to database for {player_name}: {score}")
            except Exception as e:
                print(f"Error saving to database: {e}")
                print("Falling back to in-memory storage")
                
        # Fall back to in-memory storage if database fails
        if not success:
            try:
                in_memory_scores.append({
                    'playerName': player_name,
                    'score': score,
                    'totalQuestions': len(QUESTIONS),
                    'timeTaken': time_taken,
                    'dateTaken': datetime.now().isoformat(),
                    'answers': answers
                })
                print(f"Score saved to memory for {player_name}: {score}")
                success = True
            except Exception as e:
                print(f"Error saving to memory: {e}")
        
        return jsonify({
            'score': score,
            'total': len(QUESTIONS) * 10,
            'message': 'Score saved successfully!'
        })
        
    except Exception as e:
        print(f"Error submitting quiz: {e}")
        # Even if saving fails, return the calculated score to the user
        try:
            return jsonify({
                'score': score if 'score' in locals() else 0,
                'total': len(QUESTIONS) * 10,
                'message': f'Quiz processed, but there was an error saving your score: {str(e)}'
            })
        except:
            return jsonify({
                'error': f'Error processing quiz: {str(e)}'
            }), 500

@app.route('/api/scores', methods=['GET'])
def get_scores():
    """Get top 10 scores."""
    try:
        scores = []
        
        # Try to get from database first
        if db_initialized:
            try:
                conn = get_db_connection()
                if conn:
                    if using_mysql:
                        cursor = conn.cursor(dictionary=True)
                    else:
                        cursor = conn.cursor()
                    
                    if using_mysql:
                        query = '''
                            SELECT player_name, score, total_questions, time_taken, date_taken
                            FROM quiz_scores
                            ORDER BY score DESC, time_taken ASC
                            LIMIT 10
                        '''
                    else:
                        query = '''
                            SELECT player_name, score, total_questions, time_taken, date_taken
                            FROM quiz_scores
                            ORDER BY score DESC, time_taken ASC
                            LIMIT 10
                        '''
                    
                    cursor.execute(query)
                    
                    if using_mysql:
                        db_scores = cursor.fetchall()
                    else:
                        db_scores = [dict(row) for row in cursor.fetchall()]
                    
                    conn.close()
                    
                    # Format scores from database
                    for score in db_scores:
                        if using_mysql:
                            # Convert MySQL datetime to string
                            score['date_taken'] = score['date_taken'].isoformat() if hasattr(score['date_taken'], 'isoformat') else score['date_taken']
                        scores.append({
                            'playerName': score['player_name'] if using_mysql else score['player_name'],
                            'score': score['score'],
                            'totalQuestions': score['total_questions'],
                            'timeTaken': score['time_taken'],
                            'dateTaken': score['date_taken']
                        })
            except Exception as e:
                print(f"Error getting scores from database: {e}")
        
        # Fall back to in-memory if needed
        if not scores and 'in_memory_scores' in globals():
            # Sort in-memory scores
            sorted_scores = sorted(in_memory_scores, key=lambda x: (-x['score'], x['timeTaken']))[:10]
            scores = sorted_scores
        
        return jsonify(scores)
        
    except Exception as e:
        print(f"Error getting scores: {e}")
        return jsonify([]), 500

@app.route('/api/player-scores/<player_name>', methods=['GET'])
def get_player_scores(player_name):
    """Get scores for a specific player."""
    try:
        player_scores = []
        
        # Try database first
        if db_initialized:
            try:
                conn = get_db_connection()
                if conn:
                    if using_mysql:
                        cursor = conn.cursor(dictionary=True)
                    else:
                        cursor = conn.cursor()
                    
                    query = '''
                        SELECT score, total_questions, time_taken, date_taken
                        FROM quiz_scores
                        WHERE player_name = ?
                        ORDER BY date_taken DESC
                    '''
                    
                    if using_mysql:
                        query = query.replace('?', '%s')
                    
                    cursor.execute(query, (player_name,))
                    
                    if using_mysql:
                        db_scores = cursor.fetchall()
                    else:
                        db_scores = [dict(row) for row in cursor.fetchall()]
                    
                    conn.close()
                    
                    # Format player scores from database
                    for score in db_scores:
                        if using_mysql:
                            # Convert MySQL datetime to string
                            score['date_taken'] = score['date_taken'].isoformat() if hasattr(score['date_taken'], 'isoformat') else score['date_taken']
                        player_scores.append({
                            'score': score['score'],
                            'totalQuestions': score['total_questions'],
                            'timeTaken': score['time_taken'],
                            'dateTaken': score['date_taken']
                        })
            except Exception as e:
                print(f"Error getting player scores from database: {e}")
        
        # Fall back to in-memory if needed
        if not player_scores and 'in_memory_scores' in globals():
            # Filter and sort in-memory scores for this player
            player_memory_scores = [s for s in in_memory_scores if s['playerName'] == player_name]
            sorted_scores = sorted(player_memory_scores, key=lambda x: x['dateTaken'], reverse=True)
            player_scores = sorted_scores
        
        return jsonify(player_scores)
        
    except Exception as e:
        print(f"Error getting player scores: {e}")
        return jsonify([]), 500

# Legacy routes for compatibility
@app.route('/submit-score', methods=['POST'])
def submit_score():
    try:
        data = request.json
        player_name = data.get("name", "Anonymous")
        score = data.get("score", 0)
        
        # Store score using the same mechanism as the main submit route
        current_time = datetime.now().isoformat()
        
        # Try database first
        success = False
        if db_initialized:
            try:
                conn = get_db_connection()
                if conn:
                    cursor = conn.cursor()
                    
                    if using_mysql:
                        query = '''
                            INSERT INTO quiz_scores 
                            (player_name, score, total_questions, time_taken, date_taken, answers)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        '''
                    else:
                        query = '''
                            INSERT INTO quiz_scores 
                            (player_name, score, total_questions, time_taken, date_taken, answers)
                            VALUES (?, ?, ?, ?, ?, ?)
                        '''
                    
                    cursor.execute(query, (
                        player_name,
                        score,
                        len(QUESTIONS),
                        0,  # No time data for legacy submissions
                        current_time if not using_mysql else datetime.now(),
                        '[]'  # No answers data for legacy submissions
                    ))
                    
                    conn.commit()
                    conn.close()
                    success = True
            except Exception as e:
                print(f"Error saving legacy score to database: {e}")
        
        # Fall back to in-memory
        if not success and 'in_memory_scores' in globals():
            in_memory_scores.append({
                'playerName': player_name,
                'score': score,
                'totalQuestions': len(QUESTIONS),
                'timeTaken': 0,
                'dateTaken': current_time,
                'answers': []
            })
        
        return jsonify({"message": "Score submitted successfully!"})
    except Exception as e:
        print(f"Error in legacy submit_score: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    """Legacy leaderboard route for compatibility."""
    try:
        # Reuse the scores endpoint but transform to legacy format
        scores_response = get_scores()
        scores = scores_response.json if hasattr(scores_response, 'json') else []
        
        # Convert to legacy format
        legacy_scores = [{
            'name': score.get('playerName', 'Anonymous'),
            'score': score.get('score', 0)
        } for score in scores]
        
        return jsonify(legacy_scores)
    except Exception as e:
        print(f"Error in legacy leaderboard: {e}")
        return jsonify([]), 500

# Static file routes
@app.route('/')
def serve_index():
    """Serve the index page."""
    return send_from_directory('.', 'index.html')

@app.route('/quiz')
def serve_quiz():
    """Serve the quiz page."""
    return send_from_directory('.', 'quiz.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files."""
    return send_from_directory('.', path)

@app.route('/api/add-question', methods=['POST'])
def add_question():
    """Add a new question to the system."""
    try:
        global QUESTIONS
        print("Received question submission request")
        data = request.get_json()
        if not data:
            print("Error: No data received in request")
            return jsonify({'error': 'No data received'}), 400
            
        print(f"Question data received: {data.get('question')[:30]}...")
        
        # Validate question data
        required_fields = ['question', 'options', 'correctAnswer']
        for field in required_fields:
            if field not in data:
                print(f"Error: Missing required field: {field}")
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        print("All required fields present")
        
        # Validate options array
        if not isinstance(data['options'], list) or len(data['options']) != 4:
            print("Error: Options must be an array with 4 items")
            return jsonify({'error': 'Options must be an array with 4 items'}), 400
        
        print("Options validation passed")
        
        # Validate correct answer
        if not isinstance(data['correctAnswer'], int) or data['correctAnswer'] < 0 or data['correctAnswer'] > 3:
            print("Error: Correct answer must be an integer between 0 and 3")
            return jsonify({'error': 'Correct answer must be an integer between 0 and 3'}), 400
        
        print("Correct answer validation passed")
        
        # Generate a unique ID (ensure it's unique, especially if we've deleted questions)
        next_id = 1
        if QUESTIONS:
            # Find the highest existing ID and increment by 1
            next_id = max([q.get('id', 0) for q in QUESTIONS]) + 1
        
        print(f"Generated unique ID: {next_id}")
        
        # Create new question object
        new_question = {
            "id": next_id,
            "question": data['question'],
            "options": data['options'],
            "correctAnswer": data['correctAnswer'],
            "explanation": data.get('explanation', '')
        }
        
        # Add to questions list
        QUESTIONS.append(new_question)
        print(f"Added question to in-memory list. Total questions: {len(QUESTIONS)}")
        
        # Save to file for persistence
        save_status = save_questions_to_file()
        if not save_status:
            print(f"Warning: Question '{data['question'][:30]}...' added to memory but failed to save to file")
            # But we'll still return success since the question is in memory
        
        print("Question successfully added")
        return jsonify({
            'message': 'Question added successfully',
            'question': new_question
        })
        
    except Exception as e:
        import traceback
        print(f"Error adding question: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
        
@app.route('/api/delete-question/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    """Delete a question by ID."""
    try:
        # Convert ID to int if it's numeric
        try:
            question_id = int(question_id)
        except ValueError:
            pass
            
        # Find the question by ID
        question_index = None
        for i, question in enumerate(QUESTIONS):
            if question.get('id') == question_id or i == question_id:
                question_index = i
                break
                
        if question_index is None:
            return jsonify({'error': 'Question not found'}), 404
            
        # Remove the question
        removed_question = QUESTIONS.pop(question_index)
        
        # If you have persistent storage, save changes
        save_questions_to_file()
        
        return jsonify({
            'message': 'Question deleted successfully',
            'question': removed_question
        })
        
    except Exception as e:
        print(f"Error deleting question: {e}")
        return jsonify({'error': str(e)}), 500
        
@app.route('/api/edit-question/<question_id>', methods=['PUT'])
def edit_question(question_id):
    """Edit a question by ID."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        # Convert ID to int if it's numeric
        try:
            question_id = int(question_id)
        except ValueError:
            pass
            
        # Find the question by ID
        question_index = None
        for i, question in enumerate(QUESTIONS):
            if question.get('id') == question_id or i == question_id:
                question_index = i
                break
                
        if question_index is None:
            return jsonify({'error': 'Question not found'}), 404
            
        # Update the question fields
        for field in ['question', 'options', 'correctAnswer', 'explanation']:
            if field in data:
                # Validate correct answer
                if field == 'correctAnswer' and (not isinstance(data[field], int) or data[field] < 0 or data[field] > 3):
                    return jsonify({'error': 'Correct answer must be an integer between 0 and 3'}), 400
                    
                # Validate options array
                if field == 'options' and (not isinstance(data[field], list) or len(data[field]) != 4):
                    return jsonify({'error': 'Options must be an array with 4 items'}), 400
                    
                # Update the field
                QUESTIONS[question_index][field] = data[field]
        
        # If you have persistent storage, save changes
        save_questions_to_file()
        
        return jsonify({
            'message': 'Question updated successfully',
            'question': QUESTIONS[question_index]
        })
        
    except Exception as e:
        print(f"Error updating question: {e}")
        return jsonify({'error': str(e)}), 500
        
def save_questions_to_file():
    """Save questions to a JSON file for persistence."""
    global MEMORY_ONLY_MODE
    
    if MEMORY_ONLY_MODE:
        print("Running in memory-only mode. Questions not saved to file.")
        return True
    
    try:
        # Ensure we use an absolute path to the file
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'questions.json')
        print(f"Attempting to save questions to: {file_path}")
        
        # Create directory if needed (though it should already exist)
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        # Make sure we have write permission
        try:
            # Try to create a temporary file to verify write permissions
            test_file = os.path.join(directory, '.write_test')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except Exception as perm_error:
            print(f"Warning: Directory permission test failed: {perm_error}")
            # Try the user's home directory as a fallback
            home_dir = os.path.expanduser("~")
            file_path = os.path.join(home_dir, 'questions.json')
            print(f"Falling back to home directory: {file_path}")
            
        # Actually save the file
        with open(file_path, 'w') as f:
            json.dump(QUESTIONS, f, indent=2)
        print(f"Successfully saved {len(QUESTIONS)} questions to {file_path}")
        return True
    except Exception as e:
        print(f"Error saving questions to file: {e}")
        # Try a different location as an absolute last resort
        try:
            alt_file_path = os.path.join(os.path.expanduser("~"), 'quiz_questions.json')
            with open(alt_file_path, 'w') as f:
                json.dump(QUESTIONS, f, indent=2)
            print(f"Saved to alternate location: {alt_file_path}")
            return True
        except Exception as alt_error:
            print(f"Also failed to save to alternate location: {alt_error}")
            return False
        
def load_questions_from_file():
    """Load questions from a JSON file if it exists."""
    global QUESTIONS
    try:
        # Try main location first
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'questions.json')
        if os.path.exists(file_path):
            print(f"Loading questions from: {file_path}")
            with open(file_path, 'r') as f:
                loaded_questions = json.load(f)
                if loaded_questions and isinstance(loaded_questions, list):
                    QUESTIONS = loaded_questions
                    print(f"Loaded {len(QUESTIONS)} questions from file")
                    return
                    
        # If not found, try home directory
        home_file = os.path.join(os.path.expanduser("~"), 'questions.json')
        if os.path.exists(home_file):
            print(f"Loading questions from home directory: {home_file}")
            with open(home_file, 'r') as f:
                loaded_questions = json.load(f)
                if loaded_questions and isinstance(loaded_questions, list):
                    QUESTIONS = loaded_questions
                    print(f"Loaded {len(QUESTIONS)} questions from home directory")
                    return
                    
        # Try alternative location
        alt_file = os.path.join(os.path.expanduser("~"), 'quiz_questions.json')
        if os.path.exists(alt_file):
            print(f"Loading questions from alternative location: {alt_file}")
            with open(alt_file, 'r') as f:
                loaded_questions = json.load(f)
                if loaded_questions and isinstance(loaded_questions, list):
                    QUESTIONS = loaded_questions
                    print(f"Loaded {len(QUESTIONS)} questions from alternative location")
                    return
    except Exception as e:
        print(f"Error loading questions from file: {e}")
        
# Load questions from file on startup
load_questions_from_file()

if __name__ == '__main__':
    app.run(debug=True)
