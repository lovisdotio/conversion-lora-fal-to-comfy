#!/usr/bin/env python3
"""
Verify that a LoRA file matches ComfyUI format by comparing with a reference file.

Usage:
    python verify_comfy_format.py your_file.safetensors [reference_file.safetensors]
"""

import argparse
import sys
from pathlib import Path
from safetensors.torch import load_file


def verify_format(file_path, reference_path=None):
    """Verify that a file matches ComfyUI format."""
    print(f"Loading file: {file_path}")
    
    try:
        weights = load_file(file_path)
        keys = sorted(list(weights.keys()))
    except Exception as e:
        print(f"Error loading file: {e}")
        return False
    
    print(f"Total keys: {len(keys)}")
    
    # Check format requirements
    print("\n=== Format Verification ===")
    
    # Check prefix
    all_have_diffusion_prefix = all(k.startswith("diffusion_model.") for k in keys)
    print(f"✓ All keys start with 'diffusion_model.': {all_have_diffusion_prefix}")
    
    if not all_have_diffusion_prefix:
        bad_keys = [k for k in keys if not k.startswith("diffusion_model.")]
        print(f"  Found {len(bad_keys)} keys with wrong prefix:")
        for k in bad_keys[:5]:
            print(f"    {k}")
        if len(bad_keys) > 5:
            print(f"    ... and {len(bad_keys) - 5} more")
    
    # Check lora_A and lora_B
    has_lora_A = any("lora_A.weight" in k for k in keys)
    has_lora_B = any("lora_B.weight" in k for k in keys)
    print(f"✓ Contains lora_A.weight: {has_lora_A}")
    print(f"✓ Contains lora_B.weight: {has_lora_B}")
    
    # Check for lora_down/lora_up (should NOT be present)
    has_lora_down = any("lora_down.weight" in k for k in keys)
    has_lora_up = any("lora_up.weight" in k for k in keys)
    if has_lora_down or has_lora_up:
        print(f"⚠ Contains lora_down/lora_up (should use lora_A/lora_B): {has_lora_down or has_lora_up}")
    
    # Check structure (should have dots, not underscores in paths)
    sample_key = keys[0] if keys else ""
    has_proper_structure = "." in sample_key and not sample_key.startswith("lora_unet_")
    print(f"✓ Uses dot structure (not lora_unet_*): {has_proper_structure}")
    
    # Compare with reference if provided
    if reference_path:
        print(f"\n=== Comparison with Reference ===")
        print(f"Reference file: {reference_path}")
        
        try:
            ref_weights = load_file(reference_path)
            ref_keys = sorted(list(ref_weights.keys()))
            print(f"Reference keys: {len(ref_keys)}")
            
            # Check prefix match
            ref_prefix = ref_keys[0].split(".")[0] if ref_keys else ""
            our_prefix = keys[0].split(".")[0] if keys else ""
            prefix_match = ref_prefix == our_prefix
            print(f"✓ Prefix matches reference: {prefix_match}")
            if not prefix_match:
                print(f"  Reference uses: {ref_prefix}")
                print(f"  We use:         {our_prefix}")
            
            # Check structure similarity
            if ref_keys and keys:
                ref_sample = ref_keys[0]
                our_sample = keys[0]
                print(f"\nReference sample: {ref_sample}")
                print(f"Our sample:       {our_sample}")
                
                # Check if structure matches
                ref_parts = ref_sample.split(".")
                our_parts = our_sample.split(".")
                structure_match = (
                    len(ref_parts) == len(our_parts) and
                    ref_parts[0] == our_parts[0] and
                    ref_parts[-2:] == our_parts[-2:]  # lora_A/B.weight
                )
                print(f"✓ Structure matches: {structure_match}")
        
        except Exception as e:
            print(f"Error loading reference file: {e}")
    
    print("\n=== Summary ===")
    is_valid = (
        all_have_diffusion_prefix and
        has_lora_A and
        has_lora_B and
        has_proper_structure
    )
    
    if is_valid:
        print("✓ File format is valid for ComfyUI!")
        return True
    else:
        print("✗ File format does not match ComfyUI requirements")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Verify LoRA file matches ComfyUI format"
    )
    parser.add_argument(
        "file",
        type=str,
        help="LoRA file to verify",
    )
    parser.add_argument(
        "reference",
        type=str,
        nargs="?",
        default=None,
        help="Reference ComfyUI LoRA file for comparison",
    )
    
    args = parser.parse_args()
    
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    reference_path = Path(args.reference) if args.reference else None
    if reference_path and not reference_path.exists():
        print(f"Warning: Reference file not found: {reference_path}")
        reference_path = None
    
    success = verify_format(str(file_path), str(reference_path) if reference_path else None)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()

