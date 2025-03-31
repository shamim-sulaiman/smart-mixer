@echo off
cd /d "%~dp0"
echo.
echo =============================
echo  Running Smart Mixer WebUI
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
streamlit run web_app/web_app.py

REM Pause to keep window open
echo.
echo =============================
echo  Simulation complete.
echo =============================
pause

