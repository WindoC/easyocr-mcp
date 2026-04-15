# EasyOCR MCP Server

A Model Context Protocol (MCP) server that provides OCR capabilities using the [EasyOCR](https://github.com/JaidedAI/EasyOCR) library.

> **About EasyOCR:**  
> [EasyOCR](https://github.com/JaidedAI/EasyOCR) is an open-source Optical Character Recognition (OCR) library developed by JaidedAI. It supports over 80 languages, offers GPU acceleration, and is known for its ease of use and high accuracy. EasyOCR can extract text from images, scanned documents, and photos, making it suitable for a wide range of OCR tasks. For more details, visit the [EasyOCR GitHub repository](https://github.com/JaidedAI/EasyOCR).

## Features

- **3 OCR Tools**: Process images from base64, files, or URLs
- **Multi-language Support**: Support for 80+ languages with dynamic selection
- **Flexible Output**: Choose between text-only or detailed results with coordinates and confidence
- **Performance Optimized**: Reader caching for better performance
- **Memory Controls**: Auto-unload and per-request unload options
- **Native EasyOCR Output**: Returns EasyOCR's original format

## Installation

### GPU Setup

Choose one GPU path before creating the project environment.

#### NVIDIA GPU

Use the official PyTorch install selector for your OS, Python version, and CUDA version:
- https://docs.pytorch.org/get-started/locally/

Typical Windows pip example from the PyTorch selector:

```bash
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

After install, verify:

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

#### AMD GPU

AMD GPU support depends on platform:
- Linux and WSL: use the official ROCm / Radeon PyTorch install docs
- Windows native: ROCm support exists, but AMD notes that the full ROCm stack is not yet supported on Windows

Official references:
- PyTorch local install guide: https://docs.pytorch.org/get-started/locally/
- AMD Windows compatibility matrix: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/windows/windows_compatibility.html
- AMD PyTorch install guide: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-pytorch.html

For this repository on Windows, the tested path is to reuse an existing ROCm-enabled PyTorch install in:

```bash
C:\Users\antonio\AppData\Local\Programs\Python\Python312\python.exe
```

That interpreter was verified with:

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(getattr(torch.version, 'hip', None))"
```

Expected shape of result on AMD ROCm:
- `torch.cuda.is_available()` returns `True`
- `torch.version.hip` is not `None`

### Project Environment

```bash
# Windows example used in this repo:
# C:\Users\antonio\AppData\Local\Programs\Python\Python312\python.exe
#
# Keep using uv, but create the venv from the existing Python 3.12 interpreter.
# `--system-site-packages` allows the venv to reuse packages already installed
# in that interpreter, such as an existing AMD-enabled PyTorch build.

# Create the project venv from the existing interpreter
uv venv --python C:\Users\antonio\AppData\Local\Programs\Python\Python312\python.exe --system-site-packages

# Sync this project's dependencies into the venv
uv sync

# Remove uv-installed CPU PyTorch packages so the venv falls back to the
# AMD ROCm build that already exists in Python312
uv pip uninstall torch torchvision

# Run tests through uv without re-syncing the environment
uv run --no-sync test.py
uv run --no-sync test-gpu.py
```

This keeps the project on `uv` while targeting the existing `Python312` install. Without `--system-site-packages`, a normal venv will not see packages already installed in the base interpreter. Use `uv run --no-sync` after the initial setup so `uv` does not reinstall the CPU-only PyTorch wheels from the lockfile.

## Usage

### Available Tools

1. **`ocr_image_base64`** - Process base64 encoded images
2. **`ocr_image_file`** - Process image files from disk
3. **`ocr_image_url`** - Process images from URLs
4. **`unload_ocr_models`** - Unload cached OCR models to free memory

### Parameters

- `detail`: Output detail level (default: `1`)
  - `0`: Text only - `['text1', 'text2', ...]`
  - `1`: Full details - `[([[x1,y1], [x2,y2], [x3,y3], [x4,y4]], 'text', confidence), ...]`
- `paragraph`: Enable paragraph detection (default: `false`)
- `width_ths`: Text width threshold for merging (default: `0.7`)
- `height_ths`: Text height threshold for merging (default: `0.7`)
- `unload_jobdone`: Unload models immediately after this OCR call (default: from `UNLOAD_JOBDONE`)

**Note**: Language selection is configured via the `EASYOCR_LANGUAGES` environment variable in your MCP configuration (see Configuration section below).

### Example Output

**Detail Level 1 (Full Details):**
```python
[
    ([[189, 75], [469, 75], [469, 165], [189, 165]], '愚园路', 0.3754989504814148),
    ([[86, 80], [134, 80], [134, 128], [86, 128]], '西', 0.40452659130096436)
]
```

**Detail Level 0 (Text Only):**
```python
['愚园路', '西', '东', '315', '309', 'Yuyuan Rd.', 'W', 'E']
```

## Running the Server

```bash
# Run the MCP server through uv
uv run --no-sync easyocr-mcp.py
```

## MCP Configuration Example

If you are running this as a server for a parent MCP application, you can configure it in your main MCP `config.json`.

**Windows Example:**
```json
{
  "mcpServers": {
    "easyocr-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "X:\\path\\to\\your\\project\\easyocr-mcp",
        "run",
        "easyocr-mcp.py"
      ],
      "env": {
        "EASYOCR_LANGUAGES": "en,ch_tra,ja"
      }
    }
  }
}
```

**Linux/macOS Example:**
```json
{
  "mcpServers": {
    "easyocr-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/your/project/easyocr-mcp",
        "run",
        "easyocr-mcp.py"
      ],
      "env": {
        "EASYOCR_LANGUAGES": "en,ch_tra,ja"
      }
    }
  }
}
```

### Environment Variables

- `EASYOCR_LANGUAGES`: Comma-separated list of language codes (default: `en`)
  - Examples: `en`, `en,ch_sim`, `ja,ko,en`
- `EASYOCR_UNLOAD_TIMEOUT`: Seconds of inactivity before auto-unload (default: `300`, `0` disables)
- `UNLOAD_JOBDONE`: If `true`, unload models after each OCR call by default (default: `false`)

## Supported Languages

EasyOCR supports 80+ languages including:
- `en` - English
- `ch_sim` - Chinese Simplified
- `ch_tra` - Chinese Traditional
- `ja` - Japanese
- `ko` - Korean
- `fr` - French
- `de` - German
- `es` - Spanish
- And many more...

## GPU/CPU Configuration

GPU usage is determined by the PyTorch installation visible inside the environment that launches `easyocr-mcp.py`. If you create the `uv` venv with `--system-site-packages` from `Python312`, the server can reuse the existing AMD-enabled PyTorch installed in that interpreter.

Quick verification commands:

```bash
uv run --no-sync python test-gpu.py
uv run --no-sync python test.py
uv run --no-sync python test_mcp_tools.py
```

On the verified AMD setup for this repo, `test-gpu.py` reports:
- a ROCm-enabled `torch` build
- `cuda_available=True`
- a non-empty `hip_version`
