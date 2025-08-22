#!/usr/bin/env python3
"""
Basic Argparse Example

This script demonstrates the fundamental concepts of argparse:
- Positional arguments
- Optional arguments
- Boolean flags
- Help text

Usage examples:
    python basic_argparse_example.py Alice
    python basic_argparse_example.py Alice --greeting "Hi there"
    python basic_argparse_example.py Alice --greeting "Hi there" --verbose
    python basic_argparse_example.py --help
"""

import argparse

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description='A basic example of using argparse for command-line arguments',
        epilog='Example: %(prog)s Alice --greeting "Hello" --verbose'
    )
    
    # Add positional argument (required)
    parser.add_argument('name', 
                       help='The name of the person to greet')
    
    # Add optional arguments
    parser.add_argument('-g', '--greeting', 
                       default='Hello',
                       help='Greeting message (default: %(default)s)')
    
    parser.add_argument('-v', '--verbose', 
                       action='store_true',
                       help='Enable verbose output')
    
    parser.add_argument('--uppercase', 
                       action='store_true',
                       help='Convert output to uppercase')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Create the greeting message
    message = f"{args.greeting}, {args.name}!"
    
    # Apply transformations based on arguments
    if args.uppercase:
        message = message.upper()
    
    # Output the result
    print(message)
    
    # Print additional info if verbose mode is enabled
    if args.verbose:
        print(f"Debug info:")
        print(f"  Name: {args.name}")
        print(f"  Greeting: {args.greeting}")
        print(f"  Uppercase: {args.uppercase}")
        print(f"  Verbose: {args.verbose}")

if __name__ == '__main__':
    main()