"""
WSGI entry point for production deployment
This file is used by Gunicorn to run the Flask application
"""
from dotenv import load_dotenv
import os

# Load environment variables from .env file (if exists)
load_dotenv()

from src import create_app

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    # This is only used for local development
    # For production, Gunicorn will use the 'app' object directly
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
