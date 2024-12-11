#!/bin/bash

# Get the output from the Python script
output=$(assistant "$@")

# Check if the output contains a directory change command
if [[ $output == CHANGE_DIR:* ]]; then
    # Extract the directory path and change to it
    new_dir="${output#CHANGE_DIR:}"
    cd "$new_dir"
else
    # If it's not a directory change, just echo the output
    echo "$output"
fi 