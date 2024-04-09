#!/bin/bash

# Reads to_ping.txt and returns the result of the ping test to ping_test.log

# Moves to current directory
script_dir=$(dirname "$0")
cd $script_dir

log_path="log.txt"
to_ping="to_ping.txt"

if [ ! -f "$to_ping" ]; then
    datetime=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$datetime - file not found: $script_dir/$to_ping"
    echo "$datetime - file not found: $script_dir/$to_ping" >> $log_path
    exit 1
fi

# Read names from file
names=($(cat $to_ping))

echo "log path: $script_dir/ping_test.log"

# Ping start
datetime=$(date +"%Y-%m-%d %H:%M:%S")
echo "$datetime - ping start"
echo "$datetime - ping start" >> $log_path

# Loop through each name in the list
for name in "${names[@]}"; do
    # Get the current datetime
    datetime=$(date +"%Y-%m-%d %H:%M:%S")

    # Ping the name and check the exit status
    if ping -c 1 "$name" >/dev/null 2>&1; then
        echo "$datetime - $name is available"
        echo "$datetime - $name is available" >> $log_path
    else
        echo "$datetime - $name is not available"
        echo "$datetime - $name is not available" >> $log_path
    fi
done

# Ping end
datetime=$(date +"%Y-%m-%d %H:%M:%S")
echo "$datetime - ping end"
echo "$datetime - ping end" >> $log_path