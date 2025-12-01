#!/usr/bin/env python3
"""Inspect LoRA file keys to understand the format."""

import argparse
from pathlib import Path
from safetensors.torch import load_file

def inspect_keys(file_path):
    """Load and display keys from a safetensors file."""
    print(f"Loading keys from: {file_path}")
    
    try:
        weights = load_file(file_path)
        keys = list(weights.keys())
        
        print(f"\nTotal keys: {len(keys)}")
        print(f"\nFirst 20 keys:")
        for i, key in enumerate(keys[:20], 1):
            print(f"{i:2d}. {key}")
        
        if len(keys) > 20:
            print(f"\n... and {len(keys) - 20} more keys")
            print(f"\nLast 5 keys:")
            for i, key in enumerate(keys[-5:], len(keys) - 4):
                print(f"{i:2d}. {key}")
        
        # Group keys by prefix to understand structure
        print("\n" + "="*60)
        print("Key structure analysis:")
        print("="*60)
        
        prefixes = {}
        for key in keys:
            # Get first 2-3 parts of the key
            parts = key.split(".")
            if len(parts) >= 2:
                prefix = ".".join(parts[:2])
            else:
                prefix = parts[0]
            
            if prefix not in prefixes:
                prefixes[prefix] = []
            prefixes[prefix].append(key)
        
        print(f"\nUnique prefixes (first 2 parts):")
        for prefix in sorted(prefixes.keys())[:10]:
            print(f"  {prefix}: {len(prefixes[prefix])} keys")
            # Show first example
            if prefixes[prefix]:
                print(f"    Example: {prefixes[prefix][0]}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inspect LoRA file keys")
    parser.add_argument("input", type=str, help="Input LoRA file path")
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        exit(1)
    
    inspect_keys(str(input_path))

