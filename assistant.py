#!/usr/bin/env python3
import os
import sys
import subprocess
from rich.console import Console

console = Console()

def execute_command(command, args):
    try:
        if command == ":go":
            if len(args) == 0:
                print("Error: Missing folder path", file=sys.stderr)
                return
            folder_path = os.path.expanduser(args[0])
            if os.path.isdir(folder_path):
                print(os.path.abspath(folder_path))  # Just print the path
                return
            else:
                print(f"Error: Directory does not exist: {folder_path}", file=sys.stderr)
                return
        elif command == ":fetch":
            subprocess.run(["git", "fetch"])
        elif command == ":checkout":
            if not args:
                print("Error: Missing branch name", file=sys.stderr)
                return
            subprocess.run(["git", "checkout", args[0]])
        else:
            print(f"Unknown command: {command}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: assistant :command [args]", file=sys.stderr)
        sys.exit(1)
    execute_command(sys.argv[1], sys.argv[2:])

