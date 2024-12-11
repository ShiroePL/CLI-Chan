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

# Function to fix permissions
fix_permissions() {
    local dir=$1
    echo -e "${CYAN}🔒 Setting permissions for $(basename "$dir")...${NC}"
    sudo chown -R $USER:$USER "$dir"
    if [[ "$dir" == *"/venv"* ]]; then
        # Special permissions for venv directory
        sudo find "$dir" -type d -exec chmod 755 {} \; 2>/dev/null
        sudo find "$dir" -type f -exec chmod 644 {} \; 2>/dev/null
        # Make bin files executable
        sudo find "$dir/bin" -type f -exec chmod 755 {} \; 2>/dev/null
    else
        sudo chmod -R 755 "$dir"
        # Make sure update scripts are executable
        if [ -f "$dir/update-cli-chan.sh" ]; then
            sudo chmod +x "$dir/update-cli-chan.sh"
        fi
        if [ -f "$dir/update-assistant.sh" ]; then
            sudo chmod +x "$dir/update-assistant.sh"
        fi
    fi
}

# Function to print colored messages
print_status() {
    echo -e "${CYAN}🚀 $1${NC}"
}

print_step() {
    echo -e "${YELLOW}🔄 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✨ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Redirect output to both console and log file
exec 1> >(tee -a "$REPO_DIR/update.log") 2>&1

print_status "Starting CLI-Chan Assistant update..."

# Step 1: Navigate to the repository
if [ ! -d "$REPO_DIR" ]; then
    print_error "Repository not found at $REPO_DIR"
    exit 1
fi

cd "$REPO_DIR" || exit

# Step 2: Clean old installation and set permissions
print_step "Preparing installation directory..."
sudo rm -rf "$INSTALL_DIR"
sudo mkdir -p "$INSTALL_DIR"
fix_permissions "$INSTALL_DIR"

# Step 3: Run the install script
print_step "Running installation..."
python3 "$INSTALL_SCRIPT" || { print_error "Install script failed"; exit 1; }

# Final permission check (moved before installation success message)
print_step "Finalizing setup..."
fix_permissions "$INSTALL_DIR"
if [ -d "$VENV_DIR" ]; then
    fix_permissions "$VENV_DIR"
fi

# Make sure update script stays executable for future updates
chmod +x "$SCRIPT_DIR/update-cli-chan.sh"
echo -e "${GREEN}✓ Update scripts are executable${NC}"

print_success "CLI-Chan Assistant successfully updated!"
