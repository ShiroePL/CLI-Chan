#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def setup_cli_chan():
    # Create installation directory
    install_dir = Path.home() / ".cli-chan"
    install_dir.mkdir(exist_ok=True)
    
    # Create and activate virtual environment
    venv_path = install_dir / "venv"
    if not venv_path.exists():
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)])
    
    # Install requirements
    pip_path = venv_path / "bin" / "pip"
    subprocess.run([str(pip_path), "install", "rich"])
    
    # Check if requirements need updating
    requirements_path = Path(__file__).parent / "requirements.txt"
    installed_requirements = set()
    
    # Get currently installed packages
    result = subprocess.run(
        [str(pip_path), "freeze"],
        capture_output=True,
        text=True
    )
    for line in result.stdout.splitlines():
        pkg = line.split('==')[0]
        installed_requirements.add(pkg.lower())
    
    # Check if any new requirements need to be installed
    with open(requirements_path) as f:
        required = set(
            line.split('==')[0].lower() 
            for line in f.readlines() 
            if line.strip() and not line.startswith('#')
        )
    
    missing_requirements = required - installed_requirements
    if missing_requirements:
        print("Installing missing requirements:", missing_requirements)
        subprocess.run([str(pip_path), "install", "-r", str(requirements_path)])
    else:
        print("All requirements are already installed!")
    
    # Create symlink to assistant.py
    src_path = Path(__file__).parent / "assistant.py"
    bin_path = Path.home() / ".local" / "bin" / "cli-chan"
    bin_path.parent.mkdir(exist_ok=True)
    
    if bin_path.exists():
        bin_path.unlink()
    bin_path.symlink_to(src_path)
    
    print("CLI-Chan installed successfully!")

if __name__ == "__main__":
    setup_cli_chan() 