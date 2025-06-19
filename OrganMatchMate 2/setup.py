#!/usr/bin/env python3
"""
Installation script for the Organ Donation Matching System.
This script will create a clean environment and install all the required dependencies.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def print_step(message):
    """Print a step message with formatting."""
    print(f"\n\033[1;36m==>\033[0m \033[1m{message}\033[0m")

def print_success(message):
    """Print a success message with formatting."""
    print(f"\033[1;32m✓ {message}\033[0m")

def print_error(message):
    """Print an error message with formatting."""
    print(f"\033[1;31m✗ {message}\033[0m")

def print_warning(message):
    """Print a warning message with formatting."""
    print(f"\033[1;33m! {message}\033[0m")

def check_python_version():
    """Check Python version."""
    print_step("Checking Python version")
    version = platform.python_version()
    print(f"Python version: {version}")
    major, minor, _ = version.split('.')
    if int(major) < 3 or (int(major) == 3 and int(minor) < 7):
        print_error("Python 3.7 or higher is required")
        sys.exit(1)
    else:
        print_success("Python version is compatible")

def check_pip():
    """Check if pip is installed."""
    print_step("Checking pip installation")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
        print_success("pip is installed")
        return True
    except subprocess.CalledProcessError:
        print_error("pip is not installed")
        return False

def install_dependencies():
    """Install all required dependencies."""
    print_step("Installing dependencies")
    requirements = [
        "flask==2.0.1",
        "flask-login==0.5.0",
        "flask-sqlalchemy==2.5.1",
        "flask-wtf==1.0.1",
        "sqlalchemy==1.4.23",
        "werkzeug==2.0.1",
        "wtforms==3.0.0",
        "email-validator==1.1.3",
        "gunicorn==20.1.0",
        "psycopg2-binary==2.9.1",
        "python-dotenv==0.19.0",
    ]
    
    try:
        for req in requirements:
            print(f"Installing {req}")
            subprocess.run([sys.executable, "-m", "pip", "install", req], check=True)
        print_success("All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Error installing dependencies: {e}")
        return False

def create_env_file():
    """Create a .env file if it doesn't exist."""
    print_step("Creating environment file")
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("# Environment variables for Organ Donation Matching System\n")
            f.write("FLASK_APP=main.py\n")
            f.write("FLASK_ENV=development\n")
            f.write("FLASK_DEBUG=1\n")
            f.write("SESSION_SECRET=" + os.urandom(24).hex() + "\n")
            # Use DATABASE_URL from environment if available, otherwise use default
            if "DATABASE_URL" in os.environ:
                f.write(f"DATABASE_URL={os.environ['DATABASE_URL']}\n")
            else:
                f.write("# DATABASE_URL=postgresql://username:password@localhost/dbname\n")
        print_success("Created .env file with environment variables")
    else:
        print_warning(".env file already exists, skipping")

def start_server():
    """Start the development server."""
    print_step("Starting the development server")
    try:
        if os.name != "nt":  # not on Windows
            print("Using gunicorn server (Linux/Mac)")
            subprocess.run(["gunicorn", "--bind", "0.0.0.0:5000", "--reload", "main:app"])
        else:
            print("Using Flask's built-in server (Windows)")
            os.environ["FLASK_APP"] = "main.py"
            subprocess.run([sys.executable, "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"])
    except KeyboardInterrupt:
        print("\n")
        print_warning("Server stopped by user")
    except Exception as e:
        print_error(f"Error starting the server: {str(e)}")
        print("Please try running the server manually with:")
        if os.name != "nt":
            print("  gunicorn --bind 0.0.0.0:5000 --reload main:app")
        else:
            print("  flask run --host=0.0.0.0 --port=5000")

def main():
    """Main function."""
    print("\033[1;35m" + "=" * 80 + "\033[0m")
    print("\033[1;35m Organ Donation Matching System - Installation Script \033[0m")
    print("\033[1;35m" + "=" * 80 + "\033[0m")
    
    check_python_version()
    
    if not check_pip():
        print_error("pip is required for installation")
        sys.exit(1)
    
    if install_dependencies():
        create_env_file()
        print_success("Installation completed successfully!")
        
        # Ask if user wants to start the server
        print("\nDo you want to start the development server now? (y/n)")
        choice = input().lower()
        if choice == 'y' or choice == 'yes':
            start_server()
        else:
            print("\nTo start the server later, run:")
            if os.name != "nt":
                print("  python3 -m gunicorn --bind 0.0.0.0:5000 --reload main:app")
            else:
                print("  python -m flask run --host=0.0.0.0 --port=5000")
    else:
        print_error("Installation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()