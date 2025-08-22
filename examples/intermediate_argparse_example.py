#!/usr/bin/env python3
"""
Intermediate Argparse Example

This script demonstrates intermediate argparse concepts:
- Different argument types (int, float, file)
- Multiple values (nargs)
- Choices
- Required optional arguments
- Argument groups
- Custom validation

Usage examples:
    python intermediate_argparse_example.py --numbers 1 2 3 4 5
    python intermediate_argparse_example.py --numbers 10 20 30 --operation sum --precision 2
    python intermediate_argparse_example.py --numbers 1 2 3 --operation average --format json
    python intermediate_argparse_example.py --help
"""

import argparse
import json
import sys

def positive_int(value):
    """Custom type for positive integers"""
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    return ivalue

def perform_operation(numbers, operation):
    """Perform the specified operation on the numbers"""
    if operation == 'sum':
        return sum(numbers)
    elif operation == 'average':
        return sum(numbers) / len(numbers)
    elif operation == 'min':
        return min(numbers)
    elif operation == 'max':
        return max(numbers)
    elif operation == 'count':
        return len(numbers)

def main():
    parser = argparse.ArgumentParser(
        description='Perform mathematical operations on a list of numbers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --numbers 1 2 3 4 5 --operation sum
  %(prog)s --numbers 10 20 30 --operation average --precision 3
  %(prog)s --numbers 5 15 25 --operation max --format json
        """
    )
    
    # Create argument groups for better organization
    input_group = parser.add_argument_group('input options')
    output_group = parser.add_argument_group('output options')
    
    # Input arguments
    input_group.add_argument('--numbers', 
                           type=float, 
                           nargs='+', 
                           required=True,
                           help='List of numbers to process (space-separated)')
    
    input_group.add_argument('--operation', 
                           choices=['sum', 'average', 'min', 'max', 'count'],
                           default='sum',
                           help='Operation to perform (default: %(default)s)')
    
    # Output arguments
    output_group.add_argument('--precision', 
                            type=positive_int,
                            default=2,
                            help='Number of decimal places for output (default: %(default)s)')
    
    output_group.add_argument('--format', 
                            choices=['text', 'json', 'csv'],
                            default='text',
                            help='Output format (default: %(default)s)')
    
    output_group.add_argument('-o', '--output-file',
                            type=argparse.FileType('w'),
                            default=sys.stdout,
                            help='Output file (default: stdout)')
    
    output_group.add_argument('-v', '--verbose', 
                            action='store_true',
                            help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Validate input
    if not args.numbers:
        parser.error("At least one number must be provided")
    
    # Perform the operation
    result = perform_operation(args.numbers, args.operation)
    
    # Format the result based on precision and type
    if args.operation == 'count':
        formatted_result = str(int(result))
    else:
        formatted_result = f"{result:.{args.precision}f}"
    
    # Prepare output based on format
    if args.format == 'text':
        output = f"Result: {formatted_result}"
        if args.verbose:
            output += f"\nOperation: {args.operation}"
            output += f"\nNumbers: {args.numbers}"
            output += f"\nCount: {len(args.numbers)}"
    
    elif args.format == 'json':
        data = {
            'result': float(formatted_result) if args.operation != 'count' else int(result),
            'operation': args.operation,
            'input_numbers': args.numbers,
            'count': len(args.numbers)
        }
        if args.verbose:
            data['precision'] = args.precision
        output = json.dumps(data, indent=2)
    
    elif args.format == 'csv':
        if args.verbose:
            output = f"operation,result,count,numbers\n{args.operation},{formatted_result},{len(args.numbers)},\"{' '.join(map(str, args.numbers))}\""
        else:
            output = f"result\n{formatted_result}"
    
    # Write output
    print(output, file=args.output_file)
    
    # Close file if it's not stdout
    if args.output_file != sys.stdout:
        args.output_file.close()
        if args.verbose:
            print(f"Output written to {args.output_file.name}", file=sys.stderr)

if __name__ == '__main__':
    main()