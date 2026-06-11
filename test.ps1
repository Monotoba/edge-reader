# Test script for Edge Reader on Windows (PowerShell)

$ErrorActionPreference = "Stop"

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host "WARNING: Virtual environment not found at .venv" -ForegroundColor Yellow
    Write-Host "Run 'setup.ps1' to set up the project first." -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Check if pytest is available
python -c "import pytest" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: pytest is not installed." -ForegroundColor Red
    Write-Host "Run 'setup.ps1' to install it." -ForegroundColor Red
    exit 1
}

Write-Host "Running tests..." -ForegroundColor Yellow
Write-Host ""

# Run pytest with all provided arguments
pytest @args

$testResult = $LASTEXITCODE

Write-Host ""
if ($testResult -eq 0) {
    Write-Host "✓ All tests passed!" -ForegroundColor Green
} else {
    Write-Host "✗ Some tests failed (exit code: $testResult)" -ForegroundColor Red
}

exit $testResult
