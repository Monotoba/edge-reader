# Setup script for Edge Reader on Windows (PowerShell)
# Creates virtual environment, installs dependencies, and sets up the project

param(
    [switch]$Force = $false
)

$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Edge Reader Setup for Windows (PowerShell)" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found $pythonVersion"
} catch {
    Write-Host "ERROR: Python is not installed." -ForegroundColor Red
    Write-Host "Please install Python 3.10 or newer from https://www.python.org/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Red
    exit 1
}

$pythonCheckResult = python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python 3.10 or newer is required." -ForegroundColor Red
    Write-Host "Current version: $pythonVersion" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Python version check passed" -ForegroundColor Green
Write-Host ""

# Create virtual environment
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists at .venv"
    if (-not $Force) {
        $response = Read-Host "Do you want to remove it and create a new one? (y/n)"
        if ($response -ne "y") {
            Write-Host "Using existing virtual environment"
        } else {
            Write-Host "Removing existing virtual environment..."
            Remove-Item -Recurse -Force .venv
            Write-Host "✓ Removed" -ForegroundColor Green
            $Force = $true
        }
    }
}

if (-not (Test-Path ".venv") -or $Force) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "Try running: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Failed to upgrade pip, continuing anyway..." -ForegroundColor Yellow
} else {
    Write-Host "✓ pip upgraded" -ForegroundColor Green
}
Write-Host ""

# Install project in editable mode with dev dependencies
Write-Host "Installing Edge Reader and dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..."
pip install -e ".[dev]"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Installation failed" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Installation complete" -ForegroundColor Green
Write-Host ""

# Verify installation
Write-Host "Verifying installation..." -ForegroundColor Yellow
python -c "import edge_reader" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Edge Reader module not found. Try running:" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  pip install -e '.[dev]'" -ForegroundColor Yellow
} else {
    Write-Host "✓ Edge Reader module found" -ForegroundColor Green
}
Write-Host ""

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Activate the virtual environment (if not already active):"
Write-Host "   .\.venv\Scripts\Activate.ps1"
Write-Host ""
Write-Host "2. Run the application:"
Write-Host "   python -m edge_reader"
Write-Host "   or: edge-reader"
Write-Host ""
Write-Host "3. Run tests:"
Write-Host "   pytest"
Write-Host ""
Write-Host "For platform-specific configuration, see SETUP.md" -ForegroundColor Yellow
Write-Host ""
