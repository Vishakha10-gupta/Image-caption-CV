@echo off
REM Windows Setup Script for Image Caption CV

echo.
echo ====================================
echo Image Caption CV - Windows Setup
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Installing PyTorch CPU version...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo.
echo Installing other dependencies...
pip install -r requirements.txt

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo To run the application:
echo   streamlit run app.py
echo.
pause
