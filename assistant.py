#!/usr/bin/env python3
import os
import sys
import site
import subprocess

# Add the virtual environment site-packages to Python path
VENV_PATH = "/usr/local/lib/cli-chan/venv"
site.addsitedir(os.path.join(VENV_PATH, "lib", "python3.8", "site-packages"))

from rich.console import Console

console = Console()

# Add version and path information
__version__ = "0.1.0"

def execute_command(command, args):
    try:
        if command == ":go":
            if len(args) == 0:
                print("Error: Missing folder path", file=sys.stderr)
                return
            folder_path = os.path.expanduser(args[0])  # Handle ~ in paths
            print(f"Debug: Checking path: {folder_path}", file=sys.stderr)
            if os.path.isdir(folder_path):
                abs_path = os.path.abspath(folder_path)
                print(f"Debug: Using absolute path: {abs_path}", file=sys.stderr)
                # Only print the change directory command to stdout
                print(f"CHANGE_DIR:{abs_path}")
                return
            else:
                print(f"Error: The folder '{folder_path}' does not exist.", file=sys.stderr)
                return
        elif command == ":fetch":
            console.print("[bold cyan]Fetching updates...[/bold cyan]")
            subprocess.run(["git", "fetch"], timeout=30)
        elif command == ":checkout":
            if len(args) == 0:
                console.print("[bold red]Error: Missing branch name[/bold red]")
                return
            branch_name = args[0]
            subprocess.run(["git", "checkout", branch_name], timeout=30)
        elif command == ":exit":
            console.print("[bold yellow]Goodbye![/bold yellow]")
            sys.exit(0)
        else:
            console.print(f"[bold red]Unknown command: {command}[/bold red]")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[bold yellow]Usage: :command [args][/bold yellow]")
        sys.exit(1)
    command = sys.argv[1]
    args = sys.argv[2:]
    execute_command(command, args)

