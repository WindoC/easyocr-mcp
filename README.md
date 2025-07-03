# EasyOCR MCP Server

A Model Context Protocol (MCP) server that provides OCR capabilities using the [EasyOCR](https://github.com/JaidedAI/EasyOCR) library.

> **About EasyOCR:**  
> [EasyOCR](https://github.com/JaidedAI/EasyOCR) is an open-source Optical Character Recognition (OCR) library developed by JaidedAI. It supports over 80 languages, offers GPU acceleration, and is known for its ease of use and high accuracy. EasyOCR can extract text from images, scanned documents, and photos, making it suitable for a wide range of OCR tasks. For more details, visit the [EasyOCR GitHub repository](https://github.com/JaidedAI/EasyOCR).

## Features

- **3 OCR Tools**: Process images from base64, files, or URLs
- **Multi-language Support**: Support for 80+ languages with dynamic selection
- **Flexible Output**: Choose between text-only or detailed results with coordinates and confidence
- **Performance Optimized**: Reader caching for better performance
- **Native EasyOCR Output**: Returns EasyOCR's original format

## Installation

```bash
# Install PyTorch with GPU support. Skip this step if you plan to use CPU only.
# For GPU support, adjust the command based on your system. For details, see: https://pytorch.org/get-started/locally/
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# Install all dependencies
uv sync

# Run tests to verify the implementation
uv run test.py
uv run test-gpu.py
```

## Usage

### Available Tools

1. **`ocr_image_base64`** - Process base64 encoded images
2. **`ocr_image_file`** - Process image files from disk
3. **`ocr_image_url`** - Process images from URLs

### Parameters

- `detail`: Output detail level (default: `1`)
  - `0`: Text only - `['text1', 'text2', ...]`
  - `1`: Full details - `[([[x1,y1], [x2,y2], [x3,y3], [x4,y4]], 'text', confidence), ...]`
- `paragraph`: Enable paragraph detection (default: `false`)
- `width_ths`: Text width threshold for merging (default: `0.7`)
- `height_ths`: Text height threshold for merging (default: `0.7`)

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
# Run the MCP server
uv run easyocr-mcp.py

# Or use mcp command
mcp run easyocr-mcp.py
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

GPU usage is determined at installation time based on your PyTorch installation. No runtime configuration needed.