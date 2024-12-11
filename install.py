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
    
    # Create installation directory and set permissions
    print("Creating installation directory...")
    subprocess.run(["sudo", "mkdir", "-p", INSTALL_DIR])
    subprocess.run(["sudo", "chown", "-R", os.environ["USER"], INSTALL_DIR])
    subprocess.run(["sudo", "chmod", "-R", "755", INSTALL_DIR])
    
    # Handle virtual environment first
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        subprocess.run(["sudo", "python3", "-m", "venv", VENV_DIR])
        # Set permissions for venv
        subprocess.run(["sudo", "chown", "-R", os.environ["USER"], VENV_DIR])
        subprocess.run(["sudo", "chmod", "-R", "755", VENV_DIR])
    
    # Copy project files - modified to handle nested directories
    current_dir = Path(__file__).parent
    print("Copying project files...")
    
    # First clean the directory except venv
    if os.path.exists(VENV_DIR):
        subprocess.run(["sudo", "find", INSTALL_DIR, "-not", "-path", f"{VENV_DIR}*", "-delete"])
    
    # Copy files individually to avoid nested directory
    for file in current_dir.glob('*'):
        if file.name != 'venv' and file.name != '.git':
            target = Path(INSTALL_DIR) / file.name
            try:
                subprocess.run(["sudo", "cp", "-R", str(file), str(target)], check=True)
                subprocess.run(["sudo", "chown", "-R", os.environ["USER"], str(target)])
                subprocess.run(["sudo", "chmod", "-R", "755", str(target)])
            except subprocess.CalledProcessError as e:
                print(f"Error copying {file.name}: {e}")
                return 1
    
    # Install requirements only if requirements.txt changed or venv doesn't exist
    print("Checking dependencies...")
    requirements_path = Path(INSTALL_DIR) / "requirements.txt"
    
    def has_requirements_changed():
        # Check if requirements.txt was modified in the last git pull
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD@{1}", "HEAD"],
            capture_output=True,
            text=True
        )
        changed_files = result.stdout.splitlines()
        return "requirements.txt" in changed_files
    
    if not os.path.exists(VENV_DIR) or has_requirements_changed():
        print("Requirements changed or venv missing, installing dependencies...")
        if requirements_path.exists():
            # Ensure pip is up to date
            subprocess.run([f"{VENV_DIR}/bin/python3", "-m", "pip", "install", "--upgrade", "pip"])
            # Install requirements without sudo
            subprocess.run([f"{VENV_DIR}/bin/pip", "install", "-r", str(requirements_path)])
        else:
            print(f"Warning: requirements.txt not found at {requirements_path}")
            return 1
    else:
        print("Requirements unchanged, skipping dependency installation")
    
    # Create symlink to assistant.py
    print("Creating symlink...")
    assistant_path = Path(INSTALL_DIR) / "assistant.py"
    if assistant_path.exists():
        subprocess.run(["sudo", "ln", "-sf", str(assistant_path), TARGET_BIN])
    else:
        print(f"Error: assistant.py not found at {assistant_path}")
        return 1
    
    # Make executable
    print("Setting permissions...")
    subprocess.run(["sudo", "chmod", "+x", TARGET_BIN])
    
    # Update the shebang line in the copied assistant.py
    print("Updating Python interpreter path...")
    try:
        with open(assistant_path, 'r') as f:
            content = f.read()
        
        new_content = f"#!/usr/bin/env {VENV_DIR}/bin/python3\n" + content[content.index('\n')+1:]
        
        with open(assistant_path, 'w') as f:
            f.write(new_content)
    except Exception as e:
        print(f"Error updating shebang: {e}")
        return 1
    
    print("CLI-Chan installed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(setup_cli_chan()) 