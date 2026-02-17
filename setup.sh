#!/bin/bash

echo "================================================"
echo "  Flask Auth System - Quick Setup"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python from https://www.python.org/downloads/"
    exit 1
fi

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo "Step 3: Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "Step 4: Initializing database..."
python init_db.py
if [ $? -ne 0 ]; then
    echo ""
    echo "WARNING: Database initialization failed"
    echo "Please ensure:"
    echo "1. PostgreSQL is running"
    echo "2. Database credentials in config.py are correct"
    echo "3. You have permission to create databases"
    echo ""
    echo "You can also create the database manually using pgAdmin"
    echo "See QUICKSTART.md for instructions"
    echo ""
fi

echo ""
echo "================================================"
echo "  Setup Complete!"
echo "================================================"
echo ""
echo "To start the application, run:"
echo "  python app.py"
echo ""
echo "Then open your browser and go to:"
echo "  http://localhost:5000"
echo ""
