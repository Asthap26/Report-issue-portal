from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import re
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Database connection function
def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(
            host=app.config['DB_HOST'],
            database=app.config['DB_NAME'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            port=app.config['DB_PORT']
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Initialize database tables
def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS userf (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Error initializing database: {e}")

# Email validation function
def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Routes
@app.route('/')
def home():
    """Render the home page"""
    return render_template('Home.html')

@app.route('/auth')
def auth():
    """Render the login/signup page"""
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    """Handle user registration"""
    try:
        # Get form data
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        # Validation
        if not username or not email or not password:
            return jsonify({
                'success': False,
                'message': 'Please fill all registration fields!'
            }), 400
        
        # Validate email format
        if not is_valid_email(email):
            return jsonify({
                'success': False,
                'message': 'Please enter a valid email address!'
            }), 400
        
        # Validate password length
        if len(password) < 6:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters!'
            }), 400
        
        # Validate username length
        if len(username) < 3:
            return jsonify({
                'success': False,
                'message': 'Username must be at least 3 characters!'
            }), 400
        
        # Connect to database
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'message': 'Database connection failed!'
            }), 500
        
        try:
            cur = conn.cursor()
            
            # Check if username already exists
            cur.execute("SELECT id FROM userf WHERE username = %s", (username,))
            if cur.fetchone():
                cur.close()
                conn.close()
                return jsonify({
                    'success': False,
                    'message': 'Username already exists!'
                }), 400
            
            # Check if email already exists
            cur.execute("SELECT id FROM userf WHERE email = %s", (email,))
            if cur.fetchone():
                cur.close()
                conn.close()
                return jsonify({
                    'success': False,
                    'message': 'Email already registered!'
                }), 400
            
            # Hash password
            password_hash = generate_password_hash(password)
            
            # Insert new user
            cur.execute(
                "INSERT INTO userf (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id",
                (username, email, password_hash)
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            
            # Store user in session
            session['user_id'] = user_id
            session['username'] = username
            
            return jsonify({
                'success': True,
                'message': 'Registration Successful!',
                'redirect': url_for('dashboard')
            }), 201
            
        except Exception as e:
            conn.rollback()
            conn.close()
            print(f"Signup error: {e}")
            return jsonify({
                'success': False,
                'message': 'Registration failed. Please try again.'
            }), 500
            
    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during registration.'
        }), 500

@app.route('/login', methods=['POST'])
def login():
    """Handle user login"""
    try:
        # Get form data
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Validation
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Please fill all login fields!'
            }), 400
        
        # Connect to database
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'message': 'Database connection failed!'
            }), 500
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # Find user by username
            cur.execute(
                "SELECT id, username, password_hash FROM userf WHERE username = %s",
                (username,)
            )
            user = cur.fetchone()
            cur.close()
            conn.close()
            
            # Check if user exists and password is correct
            if user and check_password_hash(user['password_hash'], password):
                # Store user in session
                session['user_id'] = user['id']
                session['username'] = user['username']
                
                return jsonify({
                    'success': True,
                    'message': 'Login Successful!',
                    'redirect': url_for('dashboard')
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid username or password!'
                }), 401
                
        except Exception as e:
            conn.close()
            print(f"Login error: {e}")
            return jsonify({
                'success': False,
                'message': 'Login failed. Please try again.'
            }), 500
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during login.'
        }), 500

@app.route('/dashboard')
def dashboard():
    """User dashboard - requires authentication"""
    if 'user_id' not in session:
        return redirect(url_for('auth'))
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Poppins', sans-serif;
            }}
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            }}
            .dashboard {{
                background: rgba(255, 255, 255, 0.9);
                padding: 50px;
                border-radius: 20px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                text-align: center;
            }}
            h1 {{
                color: #2d87d6;
                margin-bottom: 20px;
            }}
            p {{
                font-size: 18px;
                color: #333;
                margin-bottom: 30px;
            }}
            .logout-btn {{
                background: linear-gradient(to right, #e74c3c, #c0392b);
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 50px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                box-shadow: 0 5px 15px rgba(231, 76, 60, 0.3);
                transition: all 0.3s;
            }}
            .logout-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 7px 20px rgba(231, 76, 60, 0.4);
            }}
            .icon {{
                font-size: 60px;
                color: #2ecc71;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="dashboard">
            <i class="fas fa-check-circle icon"></i>
            <h1>Welcome, {session['username']}!</h1>
            <p>You have successfully logged in.</p>
            <form action="/logout" method="post">
                <button type="submit" class="logout-btn">
                    <i class="fas fa-sign-out-alt"></i> Logout
                </button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route('/logout', methods=['POST'])
def logout():
    """Handle user logout"""
    session.clear()
    return redirect(url_for('home'))

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'message': 'Page not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'success': False, 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize database on first run
    init_db()
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
