#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def setup_cli_chan():
    # Set installation paths
    INSTALL_DIR = "/usr/local/lib/cli-chan"
    TARGET_BIN = "/usr/local/bin/assistant"
    VENV_DIR = f"{INSTALL_DIR}/venv"
    
    # Create installation directory (requires sudo)
    print("Creating installation directory...")
    subprocess.run(["sudo", "mkdir", "-p", INSTALL_DIR])
    
    # Copy project files
    current_dir = Path(__file__).parent
    print("Copying project files...")
    subprocess.run(["sudo", "cp", "-R", str(current_dir), INSTALL_DIR])
    
    # Create virtual environment
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        subprocess.run(["sudo", "python3", "-m", "venv", VENV_DIR])
    
    # Install requirements
    print("Installing dependencies...")
    subprocess.run([f"{VENV_DIR}/bin/pip", "install", "-r", f"{INSTALL_DIR}/requirements.txt"])
    
    # Create symlink to assistant.py
    print("Creating symlink...")
    subprocess.run(["sudo", "ln", "-sf", f"{INSTALL_DIR}/assistant.py", TARGET_BIN])
    
    # Make executable
    print("Setting permissions...")
    subprocess.run(["sudo", "chmod", "+x", TARGET_BIN])
    
    print("CLI-Chan installed successfully!")

if __name__ == "__main__":
    setup_cli_chan() 