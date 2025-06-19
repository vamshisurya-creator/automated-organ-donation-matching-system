# Automated Organ Donation Matching System

A Flask-based web application for matching organ donors with recipients based on medical compatibility criteria.

## Features

- Registration system for organ donors and recipients
- Sophisticated matching algorithm based on blood type compatibility, urgency, and other factors
- Admin dashboard for system management
- Detailed match notifications and reports
- Secure authentication for administrators

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database (optional, can use SQLite for development)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd organ-donation-system
   ```

2. Run the installation script:
   ```
   python install.py
   ```

   The installation script will:
   - Check if your Python version is compatible
   - Install all required dependencies with the correct versions
   - Create a .env file with environment variables (if it doesn't exist)
   - Offer to start the development server

   > **Note**: If you encounter any issues with the setup.py file, please use this installation script instead. It's designed to work across different environments and Python versions.

### Manual Setup (Alternative)

If you prefer to set up the project manually:

1. Install the required dependencies with specific versions:
   ```
   pip install flask==2.0.1 flask-login==0.5.0 flask-sqlalchemy==2.5.1 flask-wtf==1.0.1 sqlalchemy==1.4.23 werkzeug==2.0.1 wtforms==3.0.0 email-validator==1.1.3 gunicorn==20.1.0 psycopg2-binary==2.9.1 python-dotenv==0.19.0
   ```

2. Create a .env file with the following variables:
   ```
   FLASK_APP=main.py
   FLASK_ENV=development
   FLASK_DEBUG=1
   SESSION_SECRET=<your-secret-key>
   DATABASE_URL=<your-database-url>
   ```

3. Start the development server:
   ```
   # On Linux/Mac:
   gunicorn --bind 0.0.0.0:5000 --reload main:app
   
   # On Windows:
   flask run --host=0.0.0.0 --port=5000
   ```

## Default Admin Credentials

The system is seeded with a default admin account:
- Username: `admin`
- Password: `adminpass`

⚠️ **Important**: Change the default admin password in production environments.

## Database Configuration

The application uses SQLAlchemy as an ORM and supports both SQLite and PostgreSQL:

- For development, SQLite is used by default
- For production, configure the PostgreSQL database connection in the .env file:
  ```
  DATABASE_URL=postgresql://username:password@localhost/dbname
  ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.