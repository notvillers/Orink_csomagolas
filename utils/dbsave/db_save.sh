#!/bin/bash

# Main script that runs all .sh files in the current directory.

# File's dir.
script_dir=$(dirname "$0")
cd "$script_dir"

# Log file
log_file="log.txt"

datetime=$(date +"%Y-%m-%d %H:%M:%S")
echo "$datetime - script started"
echo "$datetime - script started" >> $log_file

# Read all .sh files from current directory
sh_files=$(ls *.sh)

# Loop through each .sh file
for file in $sh_files; do
    # Skip the current script file and example.sh
    if [ "$file" != "$(basename "$0")" ] && [ "$file" != "example.sh" ]; then
        # Remove the .sh extension
        file_name=$(basename "$file" .sh)
        # Print the file name without the .sh extension
        datetime=$(date +"%Y-%m-%d %H:%M:%S")
        echo "$datetime - fetching $file_name"
        echo "$datetime - fetching $file_name" >> $log_file
        # Execute the script and redirect the output to the log file
        bash $file
    fi
done

datetime=$(date +"%Y-%m-%d %H:%M:%S")
echo "$datetime - script finished"
echo "$datetime - script finished" >> $log_file