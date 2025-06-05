@echo off
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.x from https://www.python.org/
    exit /b
)
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install ntplib
echo Installation complete. To run the server, activate the venv and run:
echo python time_server.py
