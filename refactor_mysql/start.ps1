# File's dir.
$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

# Activating .venv
.\.venv\Scripts\Activate.ps1
# Starting WSGI
waitress-serve --listen *:9000 webapp:app