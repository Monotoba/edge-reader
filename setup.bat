@echo off
REM Setup script for Edge Reader on Windows (Command Prompt)
REM Creates virtual environment, installs dependencies, and sets up the project

setlocal enabledelayedexpansion

echo ==================================================
echo Edge Reader Setup for Windows (Command Prompt)
echo ==================================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed.
    echo Please install Python 3.10 or newer from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.10 or newer is required.
    echo Current version: %PYTHON_VERSION%
    exit /b 1
)
echo ^✓ Python version check passed
echo.

REM Create virtual environment
if exist ".venv" (
    echo Virtual environment already exists at .venv
    set /p RESPONSE="Do you want to remove it and create a new one? (y/n): "
    if /i "!RESPONSE!"=="y" (
        echo Removing existing virtual environment...
        rmdir /s /q .venv
        echo ^✓ Removed
    )
)

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        exit /b 1
    )
    echo ^✓ Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    exit /b 1
)
echo ^✓ Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip, continuing anyway...
)
echo ^✓ pip upgraded
echo.

REM Install project in editable mode with dev dependencies
echo Installing Edge Reader and dependencies...
echo This may take a few minutes...
pip install -e ".[dev]"
if errorlevel 1 (
    echo ERROR: Installation failed
    exit /b 1
)
echo ^✓ Installation complete
echo.

REM Verify installation
echo Verifying installation...
python -c "import edge_reader" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Edge Reader module not found. Try running:
    echo   .venv\Scripts\activate.bat
    echo   pip install -e ".[dev]"
) else (
    echo ^✓ Edge Reader module found
)
echo.

echo ==================================================
echo Setup Complete!
echo ==================================================
echo.
echo Next steps:
echo 1. Activate the virtual environment:
echo    .venv\Scripts\activate.bat
echo.
echo 2. Run the application:
echo    python -m edge_reader
echo    or: edge-reader
echo.
echo 3. Run tests:
echo    pytest
echo.
echo For platform-specific configuration, see SETUP.md
echo.

REM Keep window open if run from Explorer
pause
