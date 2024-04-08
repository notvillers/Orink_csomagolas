cd /d "%~dp0"
@echo "async run"
@echo "installing venv, if not found"
start /wait venv_install.bat
start start.bat 0