# Argparse Examples

This directory contains practical examples demonstrating different levels of argparse usage in Python.

## Examples

### 1. Basic Example (`basic_argparse_example.py`)

Demonstrates fundamental argparse concepts:
- Positional arguments
- Optional arguments with short and long forms
- Boolean flags
- Default values
- Help text

**Usage:**
```bash
python basic_argparse_example.py Alice
python basic_argparse_example.py Alice --greeting "Hi there" --verbose
python basic_argparse_example.py Alice --uppercase
```

### 2. Intermediate Example (`intermediate_argparse_example.py`)

Shows more advanced features:
- Multiple argument types (int, float)
- Multiple values (nargs)
- Choices validation
- Required optional arguments
- Argument groups
- Custom type validation
- File output

**Usage:**
```bash
python intermediate_argparse_example.py --numbers 1 2 3 4 5
python intermediate_argparse_example.py --numbers 10 20 30 --operation average --precision 3
python intermediate_argparse_example.py --numbers 5 15 25 --operation max --format json
```

### 3. Advanced Example (`advanced_argparse_example.py`)

Demonstrates complex argparse patterns:
- Subcommands (subparsers)
- Mutually exclusive groups
- Custom actions
- Configuration file support
- Complex validation
- Multiple command workflows

**Usage:**
```bash
# List directory contents
python advanced_argparse_example.py list /path/to/directory --all

# Search for files
python advanced_argparse_example.py search /path/to/directory --pattern "*.py" --recursive

# Copy files with backup
python advanced_argparse_example.py copy source.txt destination.txt --backup

# Manage configuration
python advanced_argparse_example.py config show
python advanced_argparse_example.py config set --default-editor vim
```

## Learning Path

1. Start with the **basic example** to understand fundamental concepts
2. Move to the **intermediate example** to learn about types, validation, and formatting
3. Study the **advanced example** to see how to build complex CLI tools with subcommands

Each example includes comprehensive help text accessible with the `--help` flag.