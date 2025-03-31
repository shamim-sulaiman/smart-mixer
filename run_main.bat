@echo off
cd /d "%~dp0"
echo.
echo =============================
echo  Running Smart Mixer Desktop
echo =============================
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ❌ Virtual environment not found!
    pause
    exit /b
)

REM Run the main Python script from root
python desktop_gui\main.py

REM Pause to keep window open
echo.
echo =============================
echo  Simulation complete.
echo =============================
pause

