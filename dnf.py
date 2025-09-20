#!/usr/bin/env python3
"""
DNF (Directory Name Fixer) - Consolidated safe renaming tool
Combines all DNF functionality into a single script.

Usage:
  python dnf.py 1              # Before work: exkontakt -> xk
  python dnf.py 2              # After work: sxky -> exkontakt
  python dnf.py rename <mode> <old> <new>  # Direct rename mode
  python dnf.py --help         # Show this help

Features:
- Prevents duplicate consecutive executions
- Renames files, directories, and content
- Safe mode validation and error handling
- Built-in tracking to prevent mistakes
"""

import os
import sys
import subprocess
import argparse

class DNFRenamer:
    def __init__(self, root_dir=None):
        self.root_dir = root_dir or os.path.dirname(os.path.abspath(__file__))
        self.last_cmd_file = os.path.join(self.root_dir, '.dnf_last_command')
    
    def get_last_command(self):
        """Read the last executed command ID from file"""
        if not os.path.exists(self.last_cmd_file):
            return None
        
        try:
            with open(self.last_cmd_file, 'r') as f:
                return f.read().strip()
        except Exception:
            return None

    def write_last_command(self, command_id):
        """Write the current command ID to file"""
        try:
            with open(self.last_cmd_file, 'w') as f:
                f.write(str(command_id))
        except Exception as e:
            print(f"Warning: Could not write to tracking file: {e}")

    def rename_and_replace(self, mode, old_str, new_str):
        """Core renaming functionality"""
        if mode == 1:
            final_new_str = new_str
        elif mode == 2:
            final_new_str = 's' + new_str + 'y'
        else:
            raise ValueError(f"Invalid mode: {mode}. Mode must be 1 or 2.")
        
        print(f"Mode {mode}: Replacing '{old_str}' with '{final_new_str}' in directory: {self.root_dir}")
        
        # First, rename files and directories
        for dirpath, dirnames, filenames in os.walk(self.root_dir, topdown=False):
            # Rename files
            for filename in filenames:
                if old_str in filename:
                    old_path = os.path.join(dirpath, filename)
                    new_filename = filename.replace(old_str, final_new_str)
                    new_path = os.path.join(dirpath, new_filename)
                    print(f"Renaming file: {filename} -> {new_filename}")
                    os.rename(old_path, new_path)
            
            # Rename directories
            for dirname in dirnames:
                if old_str in dirname:
                    old_dir = os.path.join(dirpath, dirname)
                    new_dir = os.path.join(dirpath, dirname.replace(old_str, final_new_str))
                    print(f"Renaming directory: {dirname} -> {dirname.replace(old_str, final_new_str)}")
                    os.rename(old_dir, new_dir)

        # Now, replace in file contents
        files_modified = 0
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if old_str in content:
                        new_content = content.replace(old_str, final_new_str)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        files_modified += 1
                        print(f"Modified content in: {os.path.relpath(file_path, self.root_dir)}")
                except Exception:
                    # Skip binary or unreadable files
                    pass
        
        print(f"Replacement complete! Modified {files_modified} files.")
        return True

    def execute_safe_command(self, command_id):
        """Execute a safe command with duplicate protection"""
        # Validate command ID
        if command_id not in ['1', '2']:
            print(f"Error: Invalid command ID '{command_id}'. Must be 1 or 2.")
            return False
        
        # Define commands
        commands = {
            '1': {
                'description': 'Before work: exkontakt -> xk',
                'mode': 1,
                'old': 'exkontakt',
                'new': 'xk'
            },
            '2': {
                'description': 'After work: sxky -> exkontakt', 
                'mode': 2,
                'old': 'sxky',
                'new': 'exkontakt'
            }
        }
        
        # Check last executed command
        last_command = self.get_last_command()
        
        if last_command == command_id:
            print(f"Error: Command {command_id} was already executed last time.")
            print("Cannot execute the same command twice in a row.")
            print(f"Last executed: Command {last_command}")
            print("Please run the other command first.")
            return False
        
        # Get command details
        cmd_details = commands[command_id]
        
        print(f"Executing Command {command_id}: {cmd_details['description']}")
        
        try:
            # Execute the renaming
            success = self.rename_and_replace(
                cmd_details['mode'],
                cmd_details['old'],
                cmd_details['new']
            )
            
            if success:
                print(f"Command {command_id} completed successfully!")
                # Update tracking file only on success
                self.write_last_command(command_id)
                return True
            else:
                print(f"Command {command_id} failed!")
                return False
                
        except Exception as e:
            print(f"Error executing command: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description='DNF (Directory Name Fixer) - Safe renaming tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dnf.py 1                    # Before work: exkontakt -> xk
  python dnf.py 2                    # After work: sxky -> exkontakt
  python dnf.py rename 1 old new     # Direct rename mode 1
  python dnf.py rename 2 old new     # Direct rename mode 2

Safe Commands:
  1 = Before work: exkontakt -> xk
  2 = After work: sxky -> exkontakt

The safe commands prevent duplicate consecutive executions and track state.
        """
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Direct rename command
    rename_parser = subparsers.add_parser('rename', help='Direct rename mode')
    rename_parser.add_argument('mode', type=int, choices=[1, 2], help='Rename mode (1=simple, 2=add s/y)')
    rename_parser.add_argument('old', help='String to replace')
    rename_parser.add_argument('new', help='Replacement string')
    
    # For backwards compatibility, also accept just the command ID
    parser.add_argument('command_id', nargs='?', help='Safe command ID (1 or 2)')
    
    args = parser.parse_args()
    
    dnf = DNFRenamer()
    
    # Handle different command formats
    if args.command == 'rename':
        # Direct rename mode
        if not args.old.strip():
            print("Error: old_string cannot be empty")
            return 1
        
        try:
            success = dnf.rename_and_replace(args.mode, args.old, args.new)
            return 0 if success else 1
        except Exception as e:
            print(f"Error: {e}")
            return 1
            
    elif args.command_id:
        # Safe command mode
        success = dnf.execute_safe_command(args.command_id)
        return 0 if success else 1
        
    else:
        # No command provided, show help
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())