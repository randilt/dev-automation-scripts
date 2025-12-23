#!/usr/bin/env python3
"""
Convert JSON translation file to CSV format.
Usage: python json_to_csv.py <input.json> [output.csv]
"""

import json
import csv
import sys
from pathlib import Path


def flatten_json(data, parent_key='', sep='.'):
    """
    Flatten nested JSON structure into dot-notation keys.
    Handles nested objects, arrays, and primitive values.
    """
    items = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            
            if isinstance(value, dict):
                items.extend(flatten_json(value, new_key, sep=sep))
            elif isinstance(value, list):
                for idx, item in enumerate(value):
                    array_key = f"{new_key}{sep}{idx}"
                    if isinstance(item, (dict, list)):
                        items.extend(flatten_json(item, array_key, sep=sep))
                    else:
                        items.append((array_key, str(item)))
            else:
                items.append((new_key, str(value)))
    
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            array_key = f"{parent_key}{sep}{idx}" if parent_key else str(idx)
            if isinstance(item, (dict, list)):
                items.extend(flatten_json(item, array_key, sep=sep))
            else:
                items.append((array_key, str(item)))
    
    else:
        items.append((parent_key, str(data)))
    
    return items


def json_to_csv(input_file, output_file=None):
    """
    Convert JSON file to CSV with 'key' and 'translation' columns.
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"Error: File '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    
    if output_file is None:
        output_file = input_path.with_suffix('.csv')
    else:
        output_file = Path(output_file)
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{input_file}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{input_file}': {e}", file=sys.stderr)
        sys.exit(1)
    
    flattened = flatten_json(data)
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['key', 'translation'])
            writer.writerows(flattened)
    except Exception as e:
        print(f"Error writing CSV file '{output_file}': {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Successfully converted '{input_file}' to '{output_file}'")
    print(f"Total rows: {len(flattened)}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python json_to_csv.py <input.json> [output.csv]", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    json_to_csv(input_file, output_file)

