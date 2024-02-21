$currentDateTime = Get-Date
$formattedDateTime = $currentDateTime.ToString("yyyy-MM-dd HH:mm:ss")
Write-Host "started: $formattedDateTime" -ForegroundColor Yellow

# File's dir.
$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition
Write-Host "file's directory: $scriptPath" -ForegroundColor Green

# Move to file's dir
Set-Location $scriptPath
Write-Host "moved to: $scriptPath" -ForegroundColor Green

# Source path
$sourcePath = "\\Fsrvr\Kozos\Informatika\Scriptsrc\csomagolas"

# Destination path
$destinationPath = "C:\Users\dszombathy\Desktop\orink csomagolas\logs"

# Moving
Push-Location $sourcePath
Copy-Item -Path *.db -Destination $destinationPath

# Popping location
Pop-Location

$currentDateTime = Get-Date
$formattedDateTime = $currentDateTime.ToString("yyyy-MM-dd HH:mm:ss")
Write-Host "finished: $formattedDateTime" -ForegroundColor Yellow 
