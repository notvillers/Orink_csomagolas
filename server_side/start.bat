cd /d "%~dp0"
if "%1" equ "0" (
    PowerShell.exe -ExecutionPolicy Bypass -File "start.ps1" 0
) else (
    PowerShell.exe -ExecutionPolicy Bypass -File "start.ps1"
)