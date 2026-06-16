@echo off
echo ============================================
echo    First-Time Setup
echo ============================================

python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ERROR: Python not found. Install from https://python.org
    pause
    exit /b 1
)

echo Installing Python packages...
pip install -r requirements.txt

echo Running database migrations...
python manage.py migrate

echo Creating admin user...
python manage.py shell -c "from users.models import User; User.objects.filter(email='admin@example.com').exists() or User.objects.create_superuser(email='admin@example.com', password='admin123', first_name='Admin', last_name='User')"

echo Loading sample data...
python seed_data.py

echo.
echo ============================================
echo  Setup complete!
echo  Run start.bat to launch the server.
echo  Admin: admin@example.com / admin123
echo ============================================
pause
