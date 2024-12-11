#!/bin/bash

# Function to handle cleanup on exit
cleanup() {
    # Reset terminal
    stty sane
    exit
}

# Set up trap for cleanup
trap cleanup EXIT INT TERM

# Get the output from the Python script with a timeout
output=$(timeout 5s assistant "$@")
exit_code=$?

# Check if the command timed out
if [ $exit_code -eq 124 ]; then
    echo "Command timed out"
    exit 1
fi

# Check if the output contains a directory change command
if [[ $output == CHANGE_DIR:* ]]; then
    # Extract the directory path and change to it
    new_dir="${output#CHANGE_DIR:}"
    if [ -d "$new_dir" ]; then
        cd "$new_dir" || echo "Failed to change directory"
    else
        echo "Directory does not exist: $new_dir"
    fi
else
    # If it's not a directory change, just echo the output
    echo "$output"
fi 