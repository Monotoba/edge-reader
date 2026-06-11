@echo off
REM Publish script for uploading to PyPI

echo.
echo 📦 Publishing Edge Reader to PyPI...
echo.

REM Check if distributions exist
if not exist "dist\" (
    echo ❌ No distribution files found. Run scripts\build.bat first
    pause
    exit /b 1
)

if not exist "dist\*" (
    echo ❌ No distribution files found. Run scripts\build.bat first
    pause
    exit /b 1
)

REM Show files
echo This will upload the following files to PyPI:
dir dist\
echo.
set /p continue="Continue? (y/n) "
if /i not "%continue%"=="y" (
    echo Cancelled.
    pause
    exit /b 0
)

REM Check for PyPI token
if "%PYPI_TOKEN%"=="" (
    echo ⚠️  PYPI_TOKEN environment variable not set.
    echo Set it with: set PYPI_TOKEN=your-token-here
    set /p token="Enter PyPI token: "
    set PYPI_TOKEN=%token%
)

REM Upload to PyPI
echo.
echo Uploading to PyPI...
python -m twine upload ^
    --username "__token__" ^
    --password "%PYPI_TOKEN%" ^
    dist\*

echo.
echo ✅ Published successfully!
echo.
echo View on PyPI: https://pypi.org/project/edge-readaloud-pyside6/

pause
