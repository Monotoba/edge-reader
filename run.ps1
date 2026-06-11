# Run script for Edge Reader on Windows (PowerShell)

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

# Check if edge_reader module is available
python -c "import edge_reader" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Edge Reader is not installed." -ForegroundColor Red
    Write-Host "Run 'setup.ps1' to install it." -ForegroundColor Red
    exit 1
}

Write-Host "Starting Edge Reader..." -ForegroundColor Green
Write-Host ""

# Run the application
python -m edge_reader @args

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Edge Reader exited with an error." -ForegroundColor Red
}
