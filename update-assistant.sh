#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Variables
REPO_DIR="$SCRIPT_DIR"
INSTALL_DIR="/usr/local/lib/cli-chan"
TARGET_BIN="/usr/local/bin/assistant"
VENV_DIR="$INSTALL_DIR/venv"
INSTALL_SCRIPT="$REPO_DIR/install.py"

# Redirect output to both console and log file
exec 1> >(tee -a "$REPO_DIR/update.log") 2>&1

echo "$(date): Starting CLI-Chan Assistant update..."

# Step 1: Navigate to the repository
if [ ! -d "$REPO_DIR" ]; then
    echo "Error: Repository not found at $REPO_DIR"
    exit 1
fi

cd "$REPO_DIR" || exit

# Step 2: Pull the latest changes from GitHub
echo "Pulling the latest changes from GitHub..."
git pull || { echo "Error: Failed to pull from GitHub"; exit 1; }

# Step 3: Clean old installation and set permissions
echo "Cleaning old installation..."
sudo rm -rf "$INSTALL_DIR"
sudo mkdir -p "$INSTALL_DIR"
sudo chown -R $USER "$INSTALL_DIR"
sudo chmod -R 755 "$INSTALL_DIR"

# Step 4: Run the install script
echo "Running install script to update dependencies and copy files..."
python3 "$INSTALL_SCRIPT" || { echo "Error: Install script failed"; exit 1; }

# Step 5: Double check virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not created properly!"
    exit 1
fi

# Step 6: Verify the symlink
if [ ! -f "$TARGET_BIN" ]; then
    echo "Error: Symlink $TARGET_BIN not found or broken!"
    exit 1
fi

# Step 7: Verify executable permissions
if [ ! -x "$TARGET_BIN" ]; then
    echo "Fixing executable permissions..."
    sudo chmod +x "$TARGET_BIN"
fi

echo "CLI-Chan Assistant successfully updated!"
