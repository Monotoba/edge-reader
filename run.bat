@echo off
REM Run script for Edge Reader on Windows (Command Prompt)

REM Check if virtual environment exists
if not exist ".venv" (
    echo WARNING: Virtual environment not found at .venv
    echo Run 'setup.bat' to set up the project first.
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    exit /b 1
)

REM Check if edge_reader module is available
python -c "import edge_reader" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Edge Reader is not installed.
    echo Run 'setup.bat' to install it.
    exit /b 1
)

echo Starting Edge Reader...
echo.

REM Run the application
python -m edge_reader %*

if errorlevel 1 (
    echo.
    echo Edge Reader exited with an error.
    pause
)
