#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path
from rich.console import Console

console = Console()

def has_requirements_changed():
    # Check if requirements.txt was modified in the last git pull
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD@{1}", "HEAD"],
        capture_output=True,
        text=True
    )
    changed_files = result.stdout.splitlines()
    return "requirements.txt" in changed_files

def setup_cli_chan():
    # Set installation paths
    INSTALL_DIR = "/usr/local/lib/cli-chan"
    TARGET_BIN = "/usr/local/bin/assistant"
    VENV_DIR = f"{INSTALL_DIR}/venv"
    
    console.print("\n[bold cyan]🚀 Setting up CLI-Chan...[/bold cyan]")
    
    # Create installation directory and set permissions
    console.print("[dim]📁 Preparing installation directory...[/dim]")
    subprocess.run(["sudo", "mkdir", "-p", INSTALL_DIR])
    subprocess.run(["sudo", "chown", "-R", os.environ["USER"], INSTALL_DIR])
    subprocess.run(["sudo", "chmod", "-R", "755", INSTALL_DIR])
    
    # Create virtual environment if it doesn't exist
    if not os.path.exists(VENV_DIR):
        console.print("[yellow]🔧 Creating virtual environment...[/yellow]")
        subprocess.run(["sudo", "python3", "-m", "venv", VENV_DIR])
        # Set proper ownership and permissions
        subprocess.run(["sudo", "chown", "-R", f"{os.environ['USER']}:{os.environ['USER']}", VENV_DIR])
        subprocess.run(["sudo", "find", VENV_DIR, "-type", "d", "-exec", "chmod", "755", "{}", ";"])
        subprocess.run(["sudo", "find", VENV_DIR, "-type", "f", "-exec", "chmod", "644", "{}", ";"])
        subprocess.run(["sudo", "find", f"{VENV_DIR}/bin", "-type", "f", "-exec", "chmod", "755", "{}", ";"])
    
    # Copy project files
    console.print("[yellow]📦 Copying project files...[/yellow]")
    current_dir = Path(__file__).parent
    
    # Clean directory except venv (silently)
    if os.path.exists(VENV_DIR):
        try:
            subprocess.run(
                ["sudo", "find", INSTALL_DIR, "-mindepth", "1", 
                 "-not", "-path", f"{VENV_DIR}*", "-delete"],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                check=True
            )
        except subprocess.CalledProcessError:
            pass
    
    # Copy files individually
    for file in current_dir.glob('*'):
        if file.name != 'venv' and file.name != '.git':
            target = Path(INSTALL_DIR) / file.name
            try:
                subprocess.run(["sudo", "cp", "-R", str(file), str(target)], 
                             check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                subprocess.run(["sudo", "chown", "-R", os.environ["USER"], str(target)],
                             stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                subprocess.run(["sudo", "chmod", "-R", "755", str(target)],
                             stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                console.print(f"[bold red]❌ Error copying {file.name}: {e}[/bold red]")
                return 1
    
    # Check and install requirements
    console.print("[yellow]📥 Checking dependencies...[/yellow]")
    requirements_path = Path(INSTALL_DIR) / "requirements.txt"
    
    if not os.path.exists(VENV_DIR) or has_requirements_changed():
        if requirements_path.exists():
            console.print("[cyan]⚡ Installing dependencies...[/cyan]")
            activate_script = f"source {VENV_DIR}/bin/activate && "
            install_cmd = f"pip install -r {requirements_path}"
            subprocess.run(activate_script + install_cmd, shell=True, executable="/bin/bash")
        else:
            console.print("[bold red]❌ Requirements.txt not found![/bold red]")
            return 1
    else:
        console.print("[dim]✓ Dependencies up to date[/dim]")
    
    # Create symlink and set permissions
    console.print("[yellow]🔗 Creating symlink...[/yellow]")
    assistant_path = Path(INSTALL_DIR) / "assistant.py"
    if assistant_path.exists():
        subprocess.run(["sudo", "ln", "-sf", str(assistant_path), TARGET_BIN])
        subprocess.run(["sudo", "chmod", "+x", TARGET_BIN])
        subprocess.run(["sudo", "chown", os.environ["USER"], TARGET_BIN])
    else:
        console.print("[bold red]❌ assistant.py not found![/bold red]")
        return 1
    
    console.print("\n[bold green]✨ CLI-Chan installed successfully![/bold green]")
    console.print("[bold cyan]🎉 You can now use the 'assistant' command![/bold cyan]\n")
    return 0

if __name__ == "__main__":
    sys.exit(setup_cli_chan()) 