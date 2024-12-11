#!/usr/bin/env /usr/local/lib/cli-chan/venv/bin/python3
import os
import sys
from rich.console import Console

console = Console()

# Add version and path information
__version__ = "0.1.0"

def execute_command(command, args):
    if command == ":go":
        if len(args) == 0:
            console.print("[bold red]Error: Missing folder name[/bold red]")
            return
        folder_path = args[0]
        if os.path.isdir(folder_path):
            os.chdir(folder_path)
            console.print(f"[bold green]Changed directory to: {os.getcwd()}[/bold green]")
        else:
            console.print(f"[bold red]Error: The folder '{folder_path}' does not exist.[/bold red]")
    elif command == ":fetch":
        console.print("[bold cyan]Fetching updates...[/bold cyan]")
        os.system("git fetch")
    elif command == ":checkout":
        if len(args) == 0:
            console.print("[bold red]Error: Missing branch name[/bold red]")
            return
        branch_name = args[0]
        os.system(f"git checkout {branch_name}")
    elif command == ":exit":
        console.print("[bold yellow]Goodbye![/bold yellow]")
        sys.exit(0)
    else:
        console.print(f"[bold red]Unknown command: {command}[/bold red]")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[bold yellow]Usage: :command [args][/bold yellow]")
        sys.exit(1)
    command = sys.argv[1]
    args = sys.argv[2:]
    execute_command(command, args)

