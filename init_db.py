"""
Database Initialization Script
Run this script to verify database connection and create tables
"""

import psycopg2
from psycopg2 import sql
from config import Config

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            database='postgres',
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
            (Config.DB_NAME,)
        )
        exists = cur.fetchone()
        
        if not exists:
            # Create database
            cur.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(Config.DB_NAME)
                )
            )
            print(f"✅ Database '{Config.DB_NAME}' created successfully!")
        else:
            print(f"ℹ️  Database '{Config.DB_NAME}' already exists.")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_tables():
    """Create tables in the database"""
    try:
        # Connect to our database
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        cur = conn.cursor()
        
        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("✅ Tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def verify_connection():
    """Verify database connection"""
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        cur.close()
        conn.close()
        
        print("✅ Database connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  Flask Auth Database Initialization")
    print("="*50 + "\n")
    
    print("Step 1: Creating database...")
    if create_database():
        print("\nStep 2: Creating tables...")
        if create_tables():
            print("\nStep 3: Verifying connection...")
            if verify_connection():
                print("\n" + "="*50)
                print("  ✅ Database setup complete!")
                print("="*50 + "\n")
                print("You can now run: python app.py")
            else:
                print("\n❌ Setup failed at connection verification.")
        else:
            print("\n❌ Setup failed at table creation.")
    else:
        print("\n❌ Setup failed at database creation.")
        print("\nPlease ensure:")
        print("1. PostgreSQL is running")
        print("2. Credentials in config.py are correct")
        print("3. User has permission to create databases")
