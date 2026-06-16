@echo off
echo ============================================
echo    Ecommerce Django Backend
echo ============================================

REM Check Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Download Python from https://python.org
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo Running migrations...
python manage.py migrate

REM Start server
echo.
echo Starting server at http://localhost:8000
echo Admin panel: http://localhost:8000/admin/
echo Admin login: admin@example.com / admin123
echo.
echo Press Ctrl+C to stop.
echo ============================================
python manage.py runserver
pause
