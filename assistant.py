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
                return 1

            # This is where you'll later add AI path finding
            # For now, let's implement a simple path finder
            search_path = args[0]
            
            # First try the exact path from current directory
            if os.path.isdir(search_path):
                print(os.path.abspath(search_path))
                return 0
                
            # Then try from home directory
            home_path = os.path.expanduser(f"~/docker/{search_path}")
            if os.path.isdir(home_path):
                print(os.path.abspath(home_path))
                return 0
                
            # Later you can add AI path finding here
            # For now, just return error
            print(f"Error: Could not find directory: {search_path}", file=sys.stderr)
            return 1
            
        elif command == ":fetch":
            subprocess.run(["git", "fetch"])
        elif command == ":checkout":
            if not args:
                print("Error: Missing branch name", file=sys.stderr)
                return 1
            subprocess.run(["git", "checkout", args[0]])
        else:
            print(f"Unknown command: {command}", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: assistant :command [args]", file=sys.stderr)
        sys.exit(1)
    execute_command(sys.argv[1], sys.argv[2:])

