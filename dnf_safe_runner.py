#!/usr/bin/env python3
"""
Safe DNF Renamer - Prevents duplicate consecutive executions
Usage: python dnf_safe_runner.py <command_id>
where command_id is:
  1 = dnf_renamer.bat 1 exkontakt xk (before work)
  2 = dnf_renamer.bat 2 sxky exkontakt (after work)
"""

import os
import sys
import subprocess

def get_last_command_file():
    """Get the path to the file that stores the last executed command"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, '.dnf_last_command')

def read_last_command():
    """Read the last executed command ID from file"""
    last_cmd_file = get_last_command_file()
    if not os.path.exists(last_cmd_file):
        return None
    
    try:
        with open(last_cmd_file, 'r') as f:
            return f.read().strip()
    except Exception:
        return None

def write_last_command(command_id):
    """Write the current command ID to file"""
    last_cmd_file = get_last_command_file()
    try:
        with open(last_cmd_file, 'w') as f:
            f.write(str(command_id))
    except Exception as e:
        print(f"Warning: Could not write to tracking file: {e}")

def get_command_details(command_id):
    """Get the command details for a given command ID"""
    commands = {
        '1': {
            'description': 'Before work: exkontakt -> xk',
            'cmd': ['dnf_renamer.bat', '1', 'exkontakt', 'xk']
        },
        '2': {
            'description': 'After work: sxky -> exkontakt', 
            'cmd': ['dnf_renamer.bat', '1', 'sxky', 'exkontakt']
        }
    }
    return commands.get(command_id)

def main():
    if len(sys.argv) != 2:
        print("Usage: python dnf_safe_runner.py <command_id>")
        print("Command IDs:")
        print("  1 = Before work: exkontakt -> xk")
        print("  2 = After work: sxky -> exkontakt")
        sys.exit(1)
    
    command_id = sys.argv[1]
    
    # Validate command ID
    if command_id not in ['1', '2']:
        print(f"Error: Invalid command ID '{command_id}'. Must be 1 or 2.")
        sys.exit(1)
    
    # Check last executed command
    last_command = read_last_command()
    
    if last_command == command_id:
        print(f"Error: Command {command_id} was already executed last time.")
        print("Cannot execute the same command twice in a row.")
        print(f"Last executed: Command {last_command}")
        print("Please run the other command first, or use --force to override.")
        sys.exit(1)
    
    # Get command details
    cmd_details = get_command_details(command_id)
    if not cmd_details:
        print(f"Error: Unknown command ID: {command_id}")
        sys.exit(1)
    
    print(f"Executing Command {command_id}: {cmd_details['description']}")
    print(f"Running: {' '.join(cmd_details['cmd'])}")
    
    # Execute the command
    script_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        result = subprocess.run(
            cmd_details['cmd'],
            cwd=script_dir,
            capture_output=True,
            text=True,
            shell=True
        )
        
        # Print output
        if result.stdout:
            print("Output:")
            print(result.stdout)
        
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"Command {command_id} completed successfully!")
            # Update tracking file only on success
            write_last_command(command_id)
        else:
            print(f"Command {command_id} failed with return code {result.returncode}")
            sys.exit(result.returncode)
            
    except Exception as e:
        print(f"Error executing command: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()