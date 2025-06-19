#!/bin/bash

# Script to initialize and run the Organ Donation Matching System

# Set up environment variables (modify as needed)
export FLASK_APP=main.py
export FLASK_DEBUG=0

# Check if DATABASE_URL is already set, otherwise set a default value
if [ -z "$DATABASE_URL" ]; then
    echo "Warning: DATABASE_URL environment variable not set."
    echo "Using sqlite database as fallback (not recommended for production)"
    export DATABASE_URL="sqlite:///database.db"
fi

# Check if SESSION_SECRET is set
if [ -z "$SESSION_SECRET" ]; then
    echo "Warning: SESSION_SECRET environment variable not set."
    echo "Using a random value (should be fixed for production use)"
    export SESSION_SECRET=$(python -c 'import secrets; print(secrets.token_hex(16))')
fi

# Ensure dependencies are installed
python -m pip install -e .

# Run the app with gunicorn
echo "Starting Organ Donation Matching System..."
gunicorn --bind 0.0.0.0:5000 --workers=2 main:app