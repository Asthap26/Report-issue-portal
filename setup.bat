@echo off
echo ================================================
echo   Flask Auth System - Quick Setup
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 3: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 4: Initializing database...
python init_db.py
if errorlevel 1 (
    echo.
    echo WARNING: Database initialization failed
    echo Please ensure:
    echo 1. PostgreSQL is running
    echo 2. Database credentials in config.py are correct
    echo 3. You have permission to create databases
    echo.
    echo You can also create the database manually using pgAdmin
    echo See QUICKSTART.md for instructions
    echo.
)

echo.
echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo To start the application, run:
echo   python app.py
echo.
echo Then open your browser and go to:
echo   http://localhost:5000
echo.
pause
