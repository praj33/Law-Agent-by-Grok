@echo off
echo ========================================
echo    Legal Agent Mobile App Launcher
echo ========================================
echo.
echo Starting Legal Agent Mobile App Interface...
echo.
echo This will launch a mobile-optimized Progressive Web App
echo interface for the Legal Agent system.
echo.
echo Access URL: http://localhost:5001
echo.
echo Features:
echo - Mobile-optimized design
echo - Progressive Web App (PWA)
echo - Add to home screen capability
echo - Touch-friendly interface
echo - Quick action buttons
echo.
echo Press Ctrl+C to stop the server
echo.
pause
echo.
echo Starting mobile server...
python mobile_app_interface.py
pause