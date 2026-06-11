@echo off
REM Build script for creating distribution packages

echo.
echo 🔨 Building Edge Reader package...
echo.

REM Clean old builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for /d %%i in (src\*.egg-info) do rmdir /s /q "%%i"

REM Install build tools if needed
echo Ensuring build tools are installed...
python -m pip install --upgrade build twine

REM Build distribution
echo Building distribution...
python -m build

echo.
echo ✅ Build complete!
echo Distribution files created in dist\
echo.
echo Files ready:
dir dist\

pause
