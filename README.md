# Flask Authentication System with PostgreSQL

A complete user authentication system with login and signup functionality using Flask and PostgreSQL database.

## 📋 Features

- ✅ User Registration (Signup)
- ✅ User Login with credential verification
- ✅ Password hashing for security (Werkzeug)
- ✅ Session management
- ✅ PostgreSQL database integration
- ✅ Input validation (frontend & backend)
- ✅ Email format validation
- ✅ Password strength validation (minimum 6 characters)
- ✅ Unique username and email enforcement
- ✅ Beautiful responsive UI with animations
- ✅ Runaway button feature for unfilled forms
- ✅ Error handling and user feedback

## 🗂️ Project Structure

```
flask_auth_app/
│
├── app.py                  # Main Flask application
├── config.py              # Database configuration
├── requirements.txt       # Python dependencies
├── database_setup.sql     # SQL queries for pgAdmin
├── README.md             # This file
│
├── templates/
│   └── index.html        # Frontend login/signup page
│
└── static/               # (for future CSS/JS files if needed)
```

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **PostgreSQL** - [Download PostgreSQL](https://www.postgresql.org/download/)
3. **pgAdmin 4** - Usually comes with PostgreSQL installation

## 📦 Installation Steps

### Step 1: Set Up PostgreSQL Database

1. **Open pgAdmin 4**

2. **Connect to PostgreSQL Server**
   - Username: `postgres`
   - Password: `dhruv` (or your PostgreSQL password)

3. **Create Database**
   - Right-click on "Databases" → Create → Database
   - Database name: `flask_auth_db`
   - Owner: `postgres`
   - Click "Save"

4. **Create Tables**
   - Open Query Tool (Right-click on `flask_auth_db` → Query Tool)
   - Open `database_setup.sql` file
   - Run the queries to create the `users` table

   OR simply run this query:
   ```sql
   CREATE TABLE IF NOT EXISTS users (
       id SERIAL PRIMARY KEY,
       username VARCHAR(80) UNIQUE NOT NULL,
       email VARCHAR(120) UNIQUE NOT NULL,
       password_hash VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

### Step 2: Set Up Python Environment

1. **Navigate to project directory**
   ```bash
   cd flask_auth_app
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Configure Database Connection

1. **Open `config.py`**

2. **Verify/Update database credentials:**
   ```python
   DB_HOST = 'localhost'
   DB_NAME = 'flask_auth_db'
   DB_USER = 'postgres'
   DB_PASSWORD = 'dhruv'  # Change this to your PostgreSQL password
   DB_PORT = '5432'
   ```

### Step 4: Run the Application

1. **Start Flask server**
   ```bash
   python app.py
   ```

2. **Open browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **You should see the login/signup page!**

## 🎯 How to Use

### Registration (Signup)

1. Click the "Sign Up" button on the right panel
2. Enter:
   - Username (minimum 3 characters)
   - Email (valid email format)
   - Password (minimum 6 characters)
3. Click "Register" button
4. On success, you'll be redirected to the dashboard

### Login

1. Click the "Sign In" button if on signup page
2. Enter:
   - Username
   - Password
3. Click "Login" button
4. On success, you'll be redirected to the dashboard

### Features in Action

- **Runaway Button**: Try hovering over the Login/Register button without filling all fields - it will run away!
- **Real-time Validation**: Frontend validates inputs before sending to backend
- **Password Toggle**: Click the eye icon to show/hide password
- **Error Messages**: Clear error messages for invalid inputs

## 🔍 Database Queries (pgAdmin)

### View All Users
```sql
SELECT id, username, email, created_at 
FROM users 
ORDER BY created_at DESC;
```

### Count Total Users
```sql
SELECT COUNT(*) as total_users FROM users;
```

### Find User by Username
```sql
SELECT id, username, email, created_at 
FROM users 
WHERE username = 'your_username';
```

### Delete a User (use carefully!)
```sql
DELETE FROM users WHERE username = 'username_to_delete';
```

## 🔐 Security Features

1. **Password Hashing**: Passwords are hashed using Werkzeug's `generate_password_hash`
2. **Session Management**: Secure session handling with Flask sessions
3. **SQL Injection Prevention**: Using parameterized queries with psycopg2
4. **Input Validation**: Both frontend and backend validation
5. **Unique Constraints**: Username and email must be unique

## 🐛 Troubleshooting

### Database Connection Error
```
Error: Database connection failed
```
**Solution**: 
- Check if PostgreSQL is running
- Verify credentials in `config.py`
- Ensure database `flask_auth_db` exists

### Port Already in Use
```
Error: Address already in use
```
**Solution**: 
- Change port in `app.py`: `app.run(debug=True, port=5001)`
- Or kill the process using port 5000

### Module Not Found Error
```
ModuleNotFoundError: No module named 'flask'
```
**Solution**: 
- Activate virtual environment
- Install dependencies: `pip install -r requirements.txt`

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Render login/signup page |
| `/signup` | POST | Register new user |
| `/login` | POST | Authenticate user |
| `/dashboard` | GET | User dashboard (requires login) |
| `/logout` | POST | Logout user |

## 🚀 Future Enhancements

- [ ] Email verification
- [ ] Password reset functionality
- [ ] Remember me option
- [ ] User profile management
- [ ] Two-factor authentication
- [ ] OAuth integration (Google, GitHub)
- [ ] Password strength meter
- [ ] Account lockout after failed attempts

## 📄 License

This project is open-source and available for educational purposes.

## 👨‍💻 Author

Created with ❤️ for learning Flask and PostgreSQL

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

---

**Happy Coding! 🎉**
