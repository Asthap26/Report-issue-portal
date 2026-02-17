-- ============================================
-- FLASK AUTH DATABASE SETUP QUERIES
-- For pgAdmin 4
-- ============================================

-- Step 1: Create the database (Run this in PostgreSQL/postgres database)
-- Right-click on "Databases" in pgAdmin and select "Create" > "Database"
-- OR run this query:

CREATE DATABASE flask_auth_db
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

-- ============================================
-- IMPORTANT: After creating the database, 
-- connect to 'flask_auth_db' before running the queries below
-- ============================================

-- Step 2: Create the users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 3: Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Step 4: Add comments for documentation
COMMENT ON TABLE users IS 'Stores user authentication information';
COMMENT ON COLUMN users.id IS 'Primary key - auto-incrementing user ID';
COMMENT ON COLUMN users.username IS 'Unique username for login';
COMMENT ON COLUMN users.email IS 'Unique email address';
COMMENT ON COLUMN users.password_hash IS 'Hashed password (never store plain text!)';
COMMENT ON COLUMN users.created_at IS 'Timestamp when user account was created';

-- ============================================
-- USEFUL QUERIES FOR TESTING AND MANAGEMENT
-- ============================================

-- View all users (passwords are hashed for security)
SELECT id, username, email, created_at FROM users ORDER BY created_at DESC;

-- Count total users
SELECT COUNT(*) as total_users FROM users;

-- Find a specific user by username
SELECT id, username, email, created_at FROM users WHERE username = 'your_username';

-- Find a specific user by email
SELECT id, username, email, created_at FROM users WHERE email = 'your_email@example.com';

-- Delete a specific user (use carefully!)
-- DELETE FROM users WHERE username = 'username_to_delete';

-- Clear all users (use very carefully!)
-- TRUNCATE TABLE users RESTART IDENTITY;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check if table exists
SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = 'users'
) as table_exists;

-- View table structure
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;

-- View all indexes on users table
SELECT 
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'users';

-- ============================================
-- SAMPLE DATA (Optional - for testing)
-- ============================================

-- Note: In production, users should register through the web interface
-- These passwords are already hashed using Werkzeug's generate_password_hash
-- The plain text passwords are shown in comments for testing purposes

-- Sample user 1 (password: test123)
-- INSERT INTO users (username, email, password_hash) 
-- VALUES ('testuser', 'test@example.com', 'scrypt:32768:8:1$...');

-- To create test users with hashed passwords, use the Flask application's signup feature
-- or use Python to generate the hash:
-- from werkzeug.security import generate_password_hash
-- print(generate_password_hash('your_password'))
