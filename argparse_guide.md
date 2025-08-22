# How to Use Argparse in Python

The `argparse` module is Python's standard library solution for creating command-line interfaces. It makes it easy to write user-friendly command-line programs by handling argument parsing, type validation, help text generation, and error handling.

## Table of Contents

1. [Basic Concepts](#basic-concepts)
2. [Getting Started](#getting-started)
3. [Adding Arguments](#adding-arguments)
4. [Argument Types](#argument-types)
5. [Optional vs Required Arguments](#optional-vs-required-arguments)
6. [Argument Groups](#argument-groups)
7. [Subcommands](#subcommands)
8. [Advanced Features](#advanced-features)
9. [Best Practices](#best-practices)
10. [Complete Examples](#complete-examples)

## Basic Concepts

`argparse` works by creating an `ArgumentParser` object, defining the arguments your program accepts, and then parsing the command-line arguments passed to your script.

Key concepts:
- **ArgumentParser**: The main object that handles parsing
- **Arguments**: Parameters your script accepts (positional and optional)
- **Actions**: What to do when an argument is encountered
- **Types**: Data type conversion for arguments
- **Help**: Automatically generated help text

## Getting Started

### Minimal Example

```python
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='A simple example program')

# Add an argument
parser.add_argument('name', help='Your name')

# Parse the arguments
args = parser.parse_args()

# Use the argument
print(f"Hello, {args.name}!")
```

Usage:
```bash
python script.py Alice
# Output: Hello, Alice!

python script.py --help
# Shows help message
```

## Adding Arguments

### Positional Arguments

Positional arguments are required and must be provided in a specific order:

```python
parser.add_argument('input_file', help='Input file path')
parser.add_argument('output_file', help='Output file path')
```

### Optional Arguments

Optional arguments start with `-` or `--` and have default values:

```python
parser.add_argument('-v', '--verbose', action='store_true', 
                   help='Enable verbose output')
parser.add_argument('-o', '--output', default='output.txt',
                   help='Output file (default: output.txt)')
```

### Short and Long Options

You can provide both short (`-v`) and long (`--verbose`) versions:

```python
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-f', '--file', required=True)
```

## Argument Types

### Basic Types

```python
# String (default)
parser.add_argument('--name', type=str)

# Integer
parser.add_argument('--count', type=int)

# Float
parser.add_argument('--rate', type=float)

# Boolean flag
parser.add_argument('--enable', action='store_true')
```

### Custom Types

```python
def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    return ivalue

parser.add_argument('--threads', type=positive_int)
```

### File Types

```python
parser.add_argument('--input', type=argparse.FileType('r'))
parser.add_argument('--output', type=argparse.FileType('w'))
```

## Optional vs Required Arguments

### Making Optional Arguments Required

```python
parser.add_argument('--config', required=True, 
                   help='Configuration file (required)')
```

### Default Values

```python
parser.add_argument('--timeout', type=int, default=30,
                   help='Timeout in seconds (default: 30)')
```

### Choices

```python
parser.add_argument('--format', choices=['json', 'xml', 'csv'],
                   default='json', help='Output format')
```

## Argument Groups

Organize related arguments into groups for better help display:

```python
parser = argparse.ArgumentParser()

# Create groups
input_group = parser.add_argument_group('input options')
output_group = parser.add_argument_group('output options')

# Add arguments to groups
input_group.add_argument('--input-file', help='Input file')
input_group.add_argument('--input-format', choices=['csv', 'json'])

output_group.add_argument('--output-file', help='Output file')
output_group.add_argument('--output-format', choices=['csv', 'json'])
```

## Subcommands

Create commands with different sets of arguments:

```python
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command', help='Available commands')

# Create parser for "create" command
create_parser = subparsers.add_parser('create', help='Create a new item')
create_parser.add_argument('name', help='Item name')
create_parser.add_argument('--type', default='default', help='Item type')

# Create parser for "delete" command
delete_parser = subparsers.add_parser('delete', help='Delete an item')
delete_parser.add_argument('name', help='Item name')
delete_parser.add_argument('--force', action='store_true', help='Force deletion')

args = parser.parse_args()

if args.command == 'create':
    print(f"Creating {args.name} of type {args.type}")
elif args.command == 'delete':
    print(f"Deleting {args.name}" + (" (forced)" if args.force else ""))
```

## Advanced Features

### Multiple Values

```python
# Accept multiple values
parser.add_argument('--files', nargs='+', help='One or more files')
parser.add_argument('--coordinates', nargs=2, type=float, help='X Y coordinates')

# Optional multiple values
parser.add_argument('--tags', nargs='*', help='Zero or more tags')
```

### Mutually Exclusive Groups

```python
group = parser.add_mutually_exclusive_group()
group.add_argument('--verbose', action='store_true')
group.add_argument('--quiet', action='store_true')
```

### Custom Actions

```python
class CustomAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # Custom logic here
        setattr(namespace, self.dest, values.upper())

parser.add_argument('--name', action=CustomAction)
```

### Environment Variable Defaults

```python
import os

parser.add_argument('--api-key', 
                   default=os.getenv('API_KEY'),
                   help='API key (can also be set via API_KEY env var)')
```

## Best Practices

### 1. Use Descriptive Help Text

```python
parser.add_argument('--timeout', type=int, default=30,
                   help='Connection timeout in seconds (default: %(default)s)')
```

### 2. Validate Arguments

```python
def validate_file(filename):
    if not os.path.isfile(filename):
        raise argparse.ArgumentTypeError(f"File not found: {filename}")
    return filename

parser.add_argument('--config', type=validate_file)
```

### 3. Use Argument Groups for Organization

```python
# Group related arguments
network_group = parser.add_argument_group('network options')
network_group.add_argument('--host')
network_group.add_argument('--port', type=int)
```

### 4. Provide Good Defaults

```python
parser.add_argument('--workers', type=int, default=4,
                   help='Number of worker processes (default: %(default)s)')
```

### 5. Handle Configuration Files

```python
import configparser

def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

parser.add_argument('--config', type=load_config,
                   help='Configuration file')
```

## Complete Examples

### Example 1: File Processing Tool

```python
#!/usr/bin/env python3
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description='Process text files with various options',
        epilog='Example: %(prog)s input.txt -o output.txt --uppercase'
    )
    
    # Positional argument
    parser.add_argument('input_file', help='Input text file')
    
    # Optional arguments
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Print verbose output')
    parser.add_argument('--uppercase', action='store_true',
                       help='Convert text to uppercase')
    parser.add_argument('--line-numbers', action='store_true',
                       help='Add line numbers')
    
    args = parser.parse_args()
    
    try:
        with open(args.input_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Process lines
    for i, line in enumerate(lines, 1):
        if args.uppercase:
            line = line.upper()
        
        if args.line_numbers:
            line = f"{i:3d}: {line}"
        
        if args.output:
            with open(args.output, 'a') as f:
                f.write(line)
        else:
            print(line, end='')
    
    if args.verbose:
        print(f"Processed {len(lines)} lines", file=sys.stderr)

if __name__ == '__main__':
    main()
```

### Example 2: Database Management Tool

```python
#!/usr/bin/env python3
import argparse

def create_user(args):
    print(f"Creating user: {args.username}")
    if args.admin:
        print("User will have admin privileges")
    if args.email:
        print(f"Email: {args.email}")

def delete_user(args):
    print(f"Deleting user: {args.username}")
    if args.force:
        print("Force deletion enabled")

def list_users(args):
    print("Listing users...")
    if args.active_only:
        print("Showing only active users")

def main():
    parser = argparse.ArgumentParser(description='Database user management')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new user')
    create_parser.add_argument('username', help='Username')
    create_parser.add_argument('--email', help='User email address')
    create_parser.add_argument('--admin', action='store_true',
                              help='Grant admin privileges')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a user')
    delete_parser.add_argument('username', help='Username to delete')
    delete_parser.add_argument('--force', action='store_true',
                              help='Force deletion without confirmation')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List users')
    list_parser.add_argument('--active-only', action='store_true',
                            help='Show only active users')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        create_user(args)
    elif args.command == 'delete':
        delete_user(args)
    elif args.command == 'list':
        list_users(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
```

## Common Patterns and Tips

### 1. Version Information

```python
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
```

### 2. Debug Mode

```python
parser.add_argument('--debug', action='store_true',
                   help='Enable debug mode')

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
```

### 3. Configuration File Support

```python
import json

def load_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)

parser.add_argument('--config', type=load_config,
                   help='JSON configuration file')
```

### 4. Dry Run Mode

```python
parser.add_argument('--dry-run', action='store_true',
                   help='Show what would be done without actually doing it')
```

This comprehensive guide covers the essential aspects of using `argparse` in Python. The module is powerful and flexible, making it the go-to choice for creating professional command-line interfaces in Python applications.