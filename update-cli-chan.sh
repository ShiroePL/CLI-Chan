#!/bin/bash

# Variables
REPO_URL="https://github.com/ShiroePL/CLI-Chan.git"
INSTALL_DIR="$HOME/docker/CLI-Chan"
UPDATE_SCRIPT="$INSTALL_DIR/update-assistant.sh"

# Colors and formatting
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}Setting up CLI-Chan...${NC}"

# Step 1: Clone or update repository
if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}Cloning repository...${NC}"
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR" || exit 1
else
    echo -e "${YELLOW}Repository exists, updating...${NC}"
    cd "$INSTALL_DIR" || exit 1
    echo "Resetting local changes..."
    git reset --hard HEAD
    git clean -fd
    git pull
fi

# Step 2: Set up and run the update script
echo -e "${YELLOW}Running update script...${NC}"
chmod +x "$UPDATE_SCRIPT"
"$UPDATE_SCRIPT"

echo -e "${GREEN}CLI-Chan setup completed!${NC}" 