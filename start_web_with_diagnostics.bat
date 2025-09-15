@echo off
title Law Agent by Grok - Web Interface

echo 🏛️ LAW AGENT BY GROK - WEB INTERFACE STARTER
echo ==================================================
echo.

echo 🔍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo 💡 Please install Python 3.8 or later
    pause
    exit /b 1
)

echo ✅ Python is available
echo.

echo 🔍 Checking requirements...
python check_requirements.py
echo.

echo 🔍 Testing agent initialization...
python test_agent_initialization.py
echo.

echo 🚀 Starting web interface...
python start_ultimate_web.py

pause