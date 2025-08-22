#!/usr/bin/env python3
"""
Advanced Argparse Example

This script demonstrates advanced argparse concepts:
- Subcommands (subparsers)
- Mutually exclusive groups
- Custom actions
- Environment variable defaults
- Configuration file support
- Complex validation

This example implements a simple file management tool with multiple commands.

Usage examples:
    python advanced_argparse_example.py list /path/to/directory
    python advanced_argparse_example.py copy source.txt destination.txt --backup
    python advanced_argparse_example.py search /path/to/directory --pattern "*.py" --recursive
    python advanced_argparse_example.py config --set-default-editor vim
    python advanced_argparse_example.py --help
"""

import argparse
import os
import sys
import json
import glob
from pathlib import Path

class ConfigAction(argparse.Action):
    """Custom action for handling configuration settings"""
    def __call__(self, parser, namespace, values, option_string=None):
        config_file = Path.home() / '.filemgr_config.json'
        
        if hasattr(namespace, 'config_command'):
            if namespace.config_command == 'show':
                self.show_config(config_file)
            elif namespace.config_command == 'reset':
                self.reset_config(config_file)
        
        setattr(namespace, self.dest, values)
    
    def show_config(self, config_file):
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            print(json.dumps(config, indent=2))
        else:
            print("No configuration file found.")
    
    def reset_config(self, config_file):
        if config_file.exists():
            config_file.unlink()
            print("Configuration reset.")
        else:
            print("No configuration file to reset.")

def load_config():
    """Load configuration from file, return defaults if not found"""
    config_file = Path.home() / '.filemgr_config.json'
    default_config = {
        'default_editor': os.getenv('EDITOR', 'nano'),
        'backup_suffix': '.bak',
        'max_depth': 10
    }
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                user_config = json.load(f)
            default_config.update(user_config)
        except (json.JSONDecodeError, IOError):
            pass
    
    return default_config

def save_config(config):
    """Save configuration to file"""
    config_file = Path.home() / '.filemgr_config.json'
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

def validate_path(path_str):
    """Validate that a path exists"""
    path = Path(path_str)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"Path does not exist: {path_str}")
    return path

def validate_positive_int(value):
    """Validate positive integer"""
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise ValueError()
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid positive integer: {value}")

def cmd_list(args, config):
    """List files in directory"""
    path = args.directory
    print(f"Listing contents of {path}:")
    
    try:
        if path.is_file():
            print(f"  {path.name} (file)")
        else:
            items = sorted(path.iterdir())
            for item in items:
                if args.all or not item.name.startswith('.'):
                    item_type = "dir" if item.is_dir() else "file"
                    size = f" ({item.stat().st_size} bytes)" if item.is_file() else ""
                    print(f"  {item.name} ({item_type}){size}")
    except PermissionError:
        print(f"Permission denied: {path}", file=sys.stderr)
        sys.exit(1)

def cmd_copy(args, config):
    """Copy files with optional backup"""
    source = args.source
    destination = args.destination
    
    if destination.exists() and args.backup:
        backup_path = destination.with_suffix(destination.suffix + config['backup_suffix'])
        print(f"Creating backup: {backup_path}")
        destination.rename(backup_path)
    
    try:
        if source.is_file():
            destination.write_bytes(source.read_bytes())
            print(f"Copied {source} to {destination}")
        else:
            print(f"Error: {source} is not a file", file=sys.stderr)
            sys.exit(1)
    except (IOError, OSError) as e:
        print(f"Copy failed: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_search(args, config):
    """Search for files matching pattern"""
    base_path = args.directory
    pattern = args.pattern
    
    print(f"Searching for '{pattern}' in {base_path}")
    
    if args.recursive:
        pattern_path = base_path / "**" / pattern
        matches = glob.glob(str(pattern_path), recursive=True)
    else:
        pattern_path = base_path / pattern
        matches = glob.glob(str(pattern_path))
    
    if matches:
        print(f"Found {len(matches)} matches:")
        for match in sorted(matches):
            print(f"  {match}")
    else:
        print("No matches found.")

def cmd_config(args, config):
    """Handle configuration commands"""
    if args.config_command == 'show':
        print(json.dumps(config, indent=2))
    elif args.config_command == 'reset':
        config_file = Path.home() / '.filemgr_config.json'
        if config_file.exists():
            config_file.unlink()
            print("Configuration reset.")
        else:
            print("No configuration file to reset.")
    elif args.config_command == 'set':
        config_file = Path.home() / '.filemgr_config.json'
        if hasattr(args, 'set_default_editor') and args.set_default_editor:
            config['default_editor'] = args.set_default_editor
            save_config(config)
            print(f"Default editor set to: {args.set_default_editor}")
        elif hasattr(args, 'set_backup_suffix') and args.set_backup_suffix:
            config['backup_suffix'] = args.set_backup_suffix
            save_config(config)
            print(f"Backup suffix set to: {args.set_backup_suffix}")
        else:
            print("No configuration option specified. Use --help for available options.")

def main():
    # Load configuration
    config = load_config()
    
    # Main parser
    parser = argparse.ArgumentParser(
        description='Advanced file management tool demonstrating argparse features',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list /home/user --all
  %(prog)s copy file1.txt file2.txt --backup
  %(prog)s search /home/user --pattern "*.py" --recursive
  %(prog)s config --set-default-editor vim
        """
    )
    
    # Global options
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    
    # Mutually exclusive group for verbosity
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument('-v', '--verbose', action='store_true',
                                help='Enable verbose output')
    verbosity_group.add_argument('-q', '--quiet', action='store_true',
                                help='Suppress output')
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List directory contents')
    list_parser.add_argument('directory', type=validate_path,
                           help='Directory to list')
    list_parser.add_argument('-a', '--all', action='store_true',
                           help='Show hidden files')
    
    # Copy command
    copy_parser = subparsers.add_parser('copy', help='Copy files')
    copy_parser.add_argument('source', type=validate_path,
                           help='Source file')
    copy_parser.add_argument('destination', type=Path,
                           help='Destination path')
    # Make backup and force mutually exclusive
    backup_group = copy_parser.add_mutually_exclusive_group()
    backup_group.add_argument('--backup', action='store_true', dest='backup',
                            help='Create backup of destination if it exists')
    backup_group.add_argument('--force', action='store_true', dest='force',
                            help='Overwrite destination without backup')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for files')
    search_parser.add_argument('directory', type=validate_path,
                             help='Directory to search')
    search_parser.add_argument('-p', '--pattern', default='*',
                             help='File pattern to search for (default: %(default)s)')
    search_parser.add_argument('-r', '--recursive', action='store_true',
                             help='Search recursively')
    search_parser.add_argument('--max-depth', type=validate_positive_int,
                             default=config['max_depth'],
                             help='Maximum search depth (default: %(default)s)')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Manage configuration')
    config_subparsers = config_parser.add_subparsers(dest='config_command')
    
    # Config show
    config_show = config_subparsers.add_parser('show', help='Show current configuration')
    
    # Config set
    config_set = config_subparsers.add_parser('set', help='Set configuration values')
    config_set.add_argument('--default-editor', dest='set_default_editor',
                          help='Set default editor')
    config_set.add_argument('--backup-suffix', dest='set_backup_suffix',
                          help='Set backup file suffix')
    
    # Config reset
    config_reset = config_subparsers.add_parser('reset', help='Reset configuration')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle case where no command is provided
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute the appropriate command
    try:
        if args.command == 'list':
            cmd_list(args, config)
        elif args.command == 'copy':
            cmd_copy(args, config)
        elif args.command == 'search':
            cmd_search(args, config)
        elif args.command == 'config':
            cmd_config(args, config)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.verbose:
            raise
        else:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()