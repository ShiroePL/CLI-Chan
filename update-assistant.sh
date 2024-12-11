#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Variables
REPO_DIR="$SCRIPT_DIR"
INSTALL_DIR="/usr/local/lib/cli-chan"
TARGET_BIN="/usr/local/bin/assistant"
VENV_DIR="$INSTALL_DIR/venv"
INSTALL_SCRIPT="$REPO_DIR/install.py"

# Colors and formatting
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
DIM='\033[2m'

# Function to print colored messages
print_status() {
    echo -e "${CYAN}$(date): $1${NC}"
}

print_step() {
    echo -e "${YELLOW}🔄 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to fix permissions
fix_permissions() {
    local dir=$1
    echo "Fixing permissions for $dir..."
    sudo chown -R $USER:$USER "$dir"
    if [[ "$dir" == *"/venv"* ]]; then
        # Special permissions for venv directory
        sudo find "$dir" -type d -exec chmod 755 {} \;
        sudo find "$dir" -type f -exec chmod 644 {} \;
        # Make bin files executable
        sudo find "$dir/bin" -type f -exec chmod 755 {} \;
    else
        sudo chmod -R 755 "$dir"
    fi
}

# Redirect output to both console and log file
exec 1> >(tee -a "$REPO_DIR/update.log") 2>&1

print_status "Starting CLI-Chan Assistant update..."

# Step 1: Navigate to the repository
if [ ! -d "$REPO_DIR" ]; then
    echo "Error: Repository not found at $REPO_DIR"
    exit 1
fi

cd "$REPO_DIR" || exit

# Step 2: Pull the latest changes from GitHub
print_step "Pulling the latest changes from GitHub..."
git pull || { echo "Error: Failed to pull from GitHub"; exit 1; }

# Fix permissions after git pull
fix_permissions "$REPO_DIR"

# Step 3: Clean old installation and set permissions
echo "Cleaning old installation..."
sudo rm -rf "$INSTALL_DIR"
sudo mkdir -p "$INSTALL_DIR"
fix_permissions "$INSTALL_DIR"

# Step 4: Run the install script
echo "Running install script to update dependencies and copy files..."
python3 "$INSTALL_SCRIPT" || { echo "Error: Install script failed"; exit 1; }

# Final permission check
fix_permissions "$INSTALL_DIR"
if [ -d "$VENV_DIR" ]; then
    fix_permissions "$VENV_DIR"
fi

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

print_success "CLI-Chan Assistant successfully updated!"
