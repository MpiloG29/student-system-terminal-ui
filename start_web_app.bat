@echo off
echo Starting Student Records Web Dashboard...
echo.
cd /d "C:\Users\CapaCITI\Desktop\student-system-terminal-ui"
echo Checking Python and Flask installation...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Flask not found. Installing...
    pip install flask
)
echo.
echo Starting web server on http://localhost:5000
echo.
python web_dashboard.py
pause
