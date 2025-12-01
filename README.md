# Flux 2 LoRA to ComfyUI Converter

A simple Python tool to convert Flux 2 trainer LoRA files to ComfyUI-compatible format. This converter handles the key format differences between Flux 2 trainer outputs and ComfyUI's expected LoRA format.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Convert your LoRA file
python convert_flux2_lora_to_comfy.py your_lora.safetensors

# Verify the conversion
python verify_comfy_format.py your_lora_comfy.safetensors
```

## Features

- ✅ Converts Flux 2 trainer LoRA format (`base_model.model.*`) to ComfyUI format (`diffusion_model.*`)
- ✅ Preserves all LoRA weights and structure
- ✅ Simple one-line conversion
- ✅ Includes verification tool to validate converted files
- ✅ Supports all Flux 2 block types (double_blocks, single_blocks, time_in, txt_in, etc.)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Setup

1. Clone this repository:
```bash
git clone <your-repo-url>
cd MultipleAngles-v2
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Conversion

Convert a Flux 2 trainer LoRA file to ComfyUI format:

```bash
python convert_flux2_lora_to_comfy.py input.safetensors
```

This creates `input_comfy.safetensors` in the same directory.

### Specify Output File

```bash
python convert_flux2_lora_to_comfy.py input.safetensors output.safetensors
```

### Verify Conversion

Verify that a converted file matches ComfyUI format:

```bash
python verify_comfy_format.py your_file.safetensors
```

Compare with a reference file:

```bash
python verify_comfy_format.py your_file.safetensors reference.safetensors
```

### Inspect LoRA Keys

Inspect the keys in a LoRA file to understand its structure:

```bash
python inspect_lora_keys.py your_file.safetensors
```

## Conversion Format

The converter performs a simple prefix replacement:

**Input format (Flux 2 trainer):**
```
base_model.model.double_blocks.0.img_attn.proj.lora_A.weight
base_model.model.single_blocks.11.linear1.lora_B.weight
```

**Output format (ComfyUI):**
```
diffusion_model.double_blocks.0.img_attn.proj.lora_A.weight
diffusion_model.single_blocks.11.linear1.lora_B.weight
```

**Key changes:**
- `base_model.model.` → `diffusion_model.`
- Everything else remains unchanged (including `lora_A`/`lora_B` and dot structure)

## Examples

### Example 1: Basic Conversion

```bash
python convert_flux2_lora_to_comfy.py anne-test-lora.safetensors
```

Output: `anne-test-lora_comfy.safetensors`

### Example 2: Custom Output Name

```bash
python convert_flux2_lora_to_comfy.py my_lora.safetensors comfyui_lora.safetensors
```

### Example 3: Verify Conversion

```bash
python verify_comfy_format.py anne-test-lora_comfy.safetensors korean_f2d_1200.safetensors
```

## Project Structure

```
MultipleAngles-v2/
├── convert_flux2_lora_to_comfy.py  # Main conversion script
├── verify_comfy_format.py          # Format verification tool
├── inspect_lora_keys.py            # Key inspection utility
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── README_CONVERSION.md            # Detailed conversion documentation
```

## How It Works

The conversion is straightforward:

1. **Load** the input LoRA file (`.safetensors` format)
2. **Replace** the prefix `base_model.model.` with `diffusion_model.` for all keys
3. **Preserve** all other aspects (LoRA naming, structure, weights)
4. **Save** the converted file

The converter maintains 100% compatibility with ComfyUI's expected format, verified against standard ComfyUI LoRA files.

## Requirements

- `safetensors>=0.4.0` - For reading/writing safetensors files
- `torch>=2.0.0` - PyTorch (for tensor operations)
- `numpy>=1.24.0` - NumPy (dependency)
- `packaging>=23.0` - Packaging utilities

## Troubleshooting

### "ModuleNotFoundError: No module named 'safetensors'"

Make sure you've installed the requirements:
```bash
pip install -r requirements.txt
```

### "Error loading file"

Ensure the input file is a valid `.safetensors` file and the path is correct.

### Verification fails

If verification fails, check:
1. The file was converted using the latest version of the converter
2. The input file is from Flux 2 trainer (not already in ComfyUI format)
3. The file isn't corrupted

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license here]

## Acknowledgments

- Format verified against `korean_f2d_1200.safetensors` reference file
- Compatible with ComfyUI's Flux model LoRA format

## Support

For issues or questions, please open an issue on GitHub.

