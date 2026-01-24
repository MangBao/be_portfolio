#!/bin/bash
# Script to test Gunicorn locally before deploying to Render

echo "🧪 Testing Gunicorn server locally..."
echo "This will start the server exactly as it runs on Render"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  .env file not found. Make sure environment variables are set."
fi

# Start Gunicorn
echo ""
echo "🚀 Starting Gunicorn server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app --reload
