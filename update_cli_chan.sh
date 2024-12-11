#!/bin/bash

# Variables
REPO_URL="https://github.com/ShiroePL/CLI-Chan.git"
INSTALL_DIR="$HOME/docker/CLI-Chan"
GIT_HOOKS_DIR="$INSTALL_DIR/.git/hooks"
POST_MERGE_HOOK="$GIT_HOOKS_DIR/post-merge"
UPDATE_SCRIPT="$INSTALL_DIR/update-assistant.sh"

echo "Setting up CLI-Chan..."

# Step 1: Clone or update repository
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Cloning repository..."
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR" || exit 1
else
    echo "Repository exists, updating..."
    cd "$INSTALL_DIR" || exit 1
    # Reset any local changes before pulling
    echo "Resetting local changes..."
    git reset --hard HEAD
    git clean -fd
    git pull
fi

# Step 2: Create hooks directory if it doesn't exist
mkdir -p "$GIT_HOOKS_DIR"

# Step 3: Copy post-merge hook from repository
if [ -f "$INSTALL_DIR/post-merge" ]; then
    echo "Installing post-merge hook..."
    cp "$INSTALL_DIR/post-merge" "$POST_MERGE_HOOK"
    chmod +x "$POST_MERGE_HOOK"
else
    echo "Error: post-merge file not found in repository"
    exit 1
fi

# Step 4: Set permissions for update script
if [ -f "$UPDATE_SCRIPT" ]; then
    echo "Setting up update script..."
    chmod +x "$UPDATE_SCRIPT"
else
    echo "Error: update-assistant.sh not found"
    exit 1
fi

# Step 5: Run initial update
echo "Running initial update..."
"$UPDATE_SCRIPT"

echo "CLI-Chan setup completed!"
echo "You can now use 'assistant' command!" 