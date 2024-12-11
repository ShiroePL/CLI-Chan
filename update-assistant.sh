#!/bin/bash

# Set variables
REPO_DIR="$HOME/docker/cli-chan"
INSTALL_DIR="/usr/local/lib/cli-chan"
TARGET_BIN="/usr/local/bin/assistant"
VENV_DIR="$INSTALL_DIR/venv"

echo "Updating CLI Assistant..."

# Step 1: Navigate to the repository
cd "$REPO_DIR" || { echo "Error: Repository not found at $REPO_DIR"; exit 1; }

# Step 2: Pull the latest changes from GitHub
echo "Pulling latest changes from GitHub..."
git pull || { echo "Error: Failed to pull from GitHub"; exit 1; }

# Step 3: Copy the entire project to the installation directory
echo "Copying project files to $INSTALL_DIR..."
sudo rm -rf "$INSTALL_DIR"  # Clean old version
sudo cp -R "$REPO_DIR" "$INSTALL_DIR" || { echo "Error: Failed to copy project files"; exit 1; }

# Step 4: Set up the virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR" || { echo "Error: Failed to create virtual environment"; exit 1; }
fi

echo "Activating virtual environment and installing dependencies..."
source "$VENV_DIR/bin/activate"
pip install -r "$INSTALL_DIR/requirements.txt" || { echo "Error: Failed to install dependencies"; exit 1; }
deactivate

# Step 5: Symlink the main script to /usr/local/bin
echo "Creating symlink for assistant.py..."
sudo ln -sf "$INSTALL_DIR/assistant.py" "$TARGET_BIN" || { echo "Error: Failed to create symlink"; exit 1; }

# Step 6: Ensure the main script is executable
echo "Ensuring $TARGET_BIN is executable..."
sudo chmod +x "$TARGET_BIN" || { echo "Error: Failed to make $TARGET_BIN executable"; exit 1; }

echo "CLI Assistant successfully updated!"
