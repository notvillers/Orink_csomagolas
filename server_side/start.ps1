# Powershell script for the run.py

$currentDateTime = Get-Date
$formattedDateTime = $currentDateTime.ToString("yyyy-MM-dd HH:mm:ss")
Write-Host "started: $formattedDateTime" -ForegroundColor Yellow

# File's dir.
$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition
Write-Host "file's directory: $scriptPath" -ForegroundColor Green

# Move to file's dir
Set-Location $scriptPath
Write-Host "moved to: $scriptPath" -ForegroundColor Green

# Check for python
$pythonPath = (Get-Command -Name python -ErrorAction SilentlyContinue)
if ($pythonPath) {
    Write-Host "python found" -ForegroundColor Green
} else {
    Write-Host "python not found" -ForegroundColor Red
    exit 1
}

# If argument1 == 0
if ($argument1 -eq 0) {
    # If "update" file found, then removing venv 
    $update_path = Join-Path -Path $scriptPath -ChildPath "update"
    if (Test-Path $update_path) {
        Write-Host "update found, removing venv" -ForegroundColor Yellow
        $venv_path = Join-Path -Path $scriptPath -ChildPath ".venv"
        Remove-Item -Path $venv_path -Recurse -Force
        Remove-Item -Path $update_path -Force
    }

    # Creating and activating venv
    $venvPath = ".venv"
    if (Test-Path $venvPath -PathType Container) {
        Write-Host "venv found" -ForegroundColor Green
        Write-Host "activating venv" -ForegroundColor Green
        .\.venv\Scripts\Activate.ps1
    } else {
        Write-Host "creating venv" -ForegroundColor Yellow
        python -m venv .venv
        Write-Host "venv created" -ForegroundColor Green
        Write-Host "activating venv" -ForegroundColor Green
        .\.venv\Scripts\Activate.ps1
        Write-Host "upgrading pip" -ForegroundColor Green
        python -m pip install --upgrade pip
        Write-Host "installing packages" -ForegroundColor Green
        pip install -r requirements.txt
        deactivate
    }
}

# Activating venv
Write-Host "activating venv" -ForegroundColor Green
.\.venv\Scripts\Activate.ps1

# Runs the script
Write-Host "script start..." -ForegroundColor Green

##### script goes here
python start.py
#####

Write-Host "...script end" -ForegroundColor Green

# Deactivates the venv
deactivate
Write-Host "venv deactivated" -ForegroundColor Green

#Removing odbc_ver_ps.py
if (Test-Path $odbc_file) {
    Write-Host "removing $odbc_file" -ForegroundColor Yellow
    Remove-Item -Path $odbc_file -Force
}

$currentDateTime = Get-Date
$formattedDateTime = $currentDateTime.ToString("yyyy-MM-dd HH:mm:ss")
Write-Host "finished: $formattedDateTime" -ForegroundColor Yellow