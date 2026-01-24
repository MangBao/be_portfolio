@echo off
REM Script to test Gunicorn server locally before deploying to Render (Windows)

echo 🧪 Testing Gunicorn server locally...
echo This will start the server exactly as it runs on Render
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ⚠️  Virtual environment not found. Creating one...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Start Gunicorn
echo.
echo 🚀 Starting Gunicorn server on http://localhost:8000
echo Press Ctrl+C to stop
echo.

gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app --reload
