#!/bin/bash

# Copies file from remote server to local computer

# Remote server details
remote_user="username"
remote_host="hostname"
remote_file="remote_file.txt"
ssh_port="22"
ssh_password="password"

# Local destination
local_dir="local_file.txt"

# Copy file from remote server to local computer
sshpass -p "${ssh_password}" scp -P "${ssh_port}" "${remote_user}@${remote_host}:${remote_file}" "${local_dir}"