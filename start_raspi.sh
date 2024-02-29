#!/bin/bash

GREEN='\033[0;32m' # ${GREEN}
RED='\033[0;31m' # ${RED}
YELLOW='\033[0;33m' # ${YELLOW}
RESET='\033[0m' # ${RESET}
current_datetime=$(date +"%Y-%m-%d %H:%M:%S")
echo -e "${GREEN}started: $current_datetime${RESET}"

# File's dir.
script_dir=$(dirname "$0")
echo -e "${GREEN}file's directory: $script_dir${RESET}"

# Move to file's dir
cd $script_dir
echo -e "${GREEN}moved to: $script_dir${RESET}"

# Looking for venv and creating it if not found
folder_path=".venv"
if [ -d "$folder_path" ]; 
    then
        echo -e "${GREEN}.venv found${RESET}"
        # Activating venv
        source .venv/bin/activate
    else
        echo -e "${GREEN}creating .venv${RESET}"
        python3 -m venv .venv
        # Activating venv
        source .venv/bin/activate
        # Upgrading pip
        pip install --upgrade pip
        # Installing packages
        echo -e "${GREEN}installing packages${RESET}"
        pip install -r requirements_raspi.txt
fi

# Runs the script
echo -e "${GREEN}script starting...${RESET}"
##### Script goes here
python start.py
#####
echo -e "${GREEN}...script ended${RESET}"

# Deactivates the venv
deactivate
echo -e "${GREEN}.venv deactivated${RESET}"

current_datetime=$(date +"%Y-%m-%d %H:%M:%S")
echo -e "${GREEN}finished: $current_datetime${RESET}"
