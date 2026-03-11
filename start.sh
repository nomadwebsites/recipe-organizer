#!/bin/bash

# Quick start script for Recipe Organizer
# For development/testing purposes

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if ! pip list | grep -q Flask; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Initialize database if it doesn't exist
if [ ! -f "recipes.db" ]; then
    echo "Initializing database..."
    python3 -c "import database; database.init_db()"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  WARNING: Please edit .env and add your ANTHROPIC_API_KEY"
    echo ""
fi

# Start the application
echo "Starting Recipe Organizer..."
echo "Access the app at: http://localhost:5000"
echo ""
python3 app.py
