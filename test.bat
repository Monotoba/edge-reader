@echo off
REM Test script for Edge Reader on Windows (Command Prompt)

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

REM Check if pytest is available
python -c "import pytest" >nul 2>&1
if errorlevel 1 (
    echo ERROR: pytest is not installed.
    echo Run 'setup.bat' to install it.
    exit /b 1
)

echo Running tests...
echo.

REM Run pytest with all provided arguments
pytest %*

if errorlevel 1 (
    echo.
    echo ✗ Some tests failed
    exit /b 1
) else (
    echo.
    echo ✓ All tests passed!
)
