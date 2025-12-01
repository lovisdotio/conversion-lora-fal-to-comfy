#!/usr/bin/env python3
"""
Convert Flux 2 trainer LoRA (base_model.model.* format) to ComfyUI format.

Usage:
    python convert_flux2_lora_to_comfy.py input.safetensors [output.safetensors]
"""

import argparse
import sys
from pathlib import Path
from safetensors.torch import load_file, save_file


def convert_to_comfy_format(input_weights):
    """
    Convert Flux 2 trainer format to ComfyUI format.
    
    ComfyUI format simply replaces 'base_model.model.' with 'diffusion_model.'
    and keeps everything else the same (including lora_A/lora_B and dot structure).
    
    Input format: base_model.model.{block_type}.{block_num}.{weight_path}.lora_{A|B}.weight
    Output format: diffusion_model.{block_type}.{block_num}.{weight_path}.lora_{A|B}.weight
    
    Examples:
        base_model.model.double_blocks.0.img_attn.proj.lora_A.weight
        -> diffusion_model.double_blocks.0.img_attn.proj.lora_A.weight
        
        base_model.model.single_blocks.11.linear1.lora_B.weight
        -> diffusion_model.single_blocks.11.linear1.lora_B.weight
    """
    comfy_weights = {}
    
    for key, tensor in input_weights.items():
        # Skip keys that don't start with base_model.model
        if not key.startswith("base_model.model."):
            print(f"Warning: Skipping key that doesn't start with 'base_model.model.': {key}")
            continue
        
        # Simply replace 'base_model.model.' with 'diffusion_model.'
        comfy_key = key.replace("base_model.model.", "diffusion_model.", 1)
        comfy_weights[comfy_key] = tensor
    
    return comfy_weights


def convert_flux2_lora_to_comfy(input_path, output_path):
    """Main conversion function."""
    print(f"Loading LoRA from: {input_path}")
    
    try:
        input_weights = load_file(input_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print(f"Loaded {len(input_weights)} keys")
    print(f"Sample input keys:")
    for key in list(input_weights.keys())[:5]:
        print(f"  {key}")
    
    print("\nConverting to ComfyUI format...")
    comfy_weights = convert_to_comfy_format(input_weights)
    
    if not comfy_weights:
        print("Error: No weights were converted!")
        return False
    
    print(f"\nConverted to {len(comfy_weights)} ComfyUI keys")
    print(f"Sample ComfyUI keys:")
    for key in list(comfy_weights.keys())[:5]:
        print(f"  {key}")
    
    print(f"\nSaving to: {output_path}")
    try:
        save_file(comfy_weights, output_path)
    except Exception as e:
        print(f"Error saving file: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\nConversion complete!")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Convert Flux 2 trainer LoRA to ComfyUI format"
    )
    parser.add_argument(
        "input",
        type=str,
        help="Input LoRA file path (Flux 2 trainer format)",
    )
    parser.add_argument(
        "output",
        type=str,
        nargs="?",
        default=None,
        help="Output LoRA file path (ComfyUI format). If not provided, adds '_comfy' suffix.",
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    if args.output:
        output_path = Path(args.output)
    else:
        # Add _comfy suffix before extension
        stem = input_path.stem
        suffix = input_path.suffix
        output_path = input_path.parent / f"{stem}_comfy{suffix}"
    
    success = convert_flux2_lora_to_comfy(str(input_path), str(output_path))
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()

