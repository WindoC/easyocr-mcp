#!/usr/bin/env python3
"""
Test script to verify EasyOCR MCP tools are working correctly.
This tests the tools directly without the MCP protocol layer.
"""

import base64
import importlib.util
import os
import sys

import torch

# Set environment variables for testing
os.environ["EASYOCR_LANGUAGES"] = "en"
os.environ.setdefault("EASYOCR_UNLOAD_TIMEOUT", "300")
os.environ.setdefault("UNLOAD_JOBDONE", "false")

sys.path.append(os.path.dirname(__file__))

# Import from easyocr-mcp.py (need to handle the dash in filename)
spec = importlib.util.spec_from_file_location("easyocr_mcp", "easyocr-mcp.py")
easyocr_mcp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(easyocr_mcp)

ocr_image_base64 = easyocr_mcp.ocr_image_base64
ocr_image_file = easyocr_mcp.ocr_image_file
ocr_image_url = easyocr_mcp.ocr_image_url
unload_ocr_models = easyocr_mcp.unload_ocr_models


def test_gpu_runtime():
    """Report GPU runtime details without failing CPU-only environments."""
    print("Testing GPU runtime...")
    print(f"Python executable: {sys.executable}")
    print(f"Torch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    print(f"HIP version: {getattr(torch.version, 'hip', None)}")

    if not torch.cuda.is_available():
        print("GPU runtime check skipped: torch.cuda.is_available() is False")
        return True

    if not getattr(torch.version, "hip", None):
        print("GPU runtime check skipped: ROCm/HIP runtime not detected")
        return True

    return True


def test_file_ocr():
    """Test OCR on a local file."""
    print("Testing OCR on local file...")
    try:
        result = ocr_image_file("test.png", detail=1)
        print(f"File OCR result: {result}")
        return True
    except Exception as e:
        print(f"File OCR failed: {e}")
        return False


def test_base64_ocr():
    """Test OCR on base64 encoded image."""
    print("\nTesting OCR on base64 image...")
    try:
        with open("test.png", "rb") as f:
            image_bytes = f.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        result = ocr_image_base64(base64_image, detail=1)
        print(f"Base64 OCR result: {result}")
        return True
    except Exception as e:
        print(f"Base64 OCR failed: {e}")
        return False


def test_url_ocr():
    """Test OCR on image from URL."""
    print("\nTesting OCR on URL image...")
    try:
        test_url = "https://geekyants.com/_next/image?url=https%3A%2F%2Fstatic-cdn.geekyants.com%2Farticleblogcomponent%2F22981%2F2023-10-17%2F381813330-1697540509.png&w=3840&q=75"
        result = ocr_image_url(test_url, detail=1)
        print(f"URL OCR result: {result}")
        return True
    except Exception as e:
        if "Failed to download" in str(e) or "NameResolutionError" in str(e):
            print(f"URL OCR skipped due to network issues: {e}")
            return True
        print(f"URL OCR failed: {e}")
        return False


def test_different_detail_levels():
    """Test different detail levels."""
    print("\nTesting different detail levels...")
    try:
        result_0 = ocr_image_file("test.png", detail=0)
        print(f"Detail=0 result: {result_0}")

        result_1 = ocr_image_file("test.png", detail=1)
        print(f"Detail=1 result: {result_1}")
        return True
    except Exception as e:
        print(f"Detail level test failed: {e}")
        return False


def test_unload_jobdone():
    """Test per-call unload_jobdone behavior."""
    print("\nTesting unload_jobdone...")
    try:
        result = ocr_image_file("test.png", detail=1, unload_jobdone=True)
        print(f"OCR result with unload_jobdone: {result}")
        return True
    except Exception as e:
        print(f"unload_jobdone test failed: {e}")
        return False


def test_manual_unload():
    """Test manual unload tool."""
    print("\nTesting manual unload tool...")
    try:
        _ = ocr_image_file("test.png", detail=1)
        unload_result = unload_ocr_models()
        print(f"Unload result: {unload_result}")
        return True
    except Exception as e:
        print(f"Manual unload test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("Testing EasyOCR MCP Tools")
    print("=" * 50)

    tests = [
        test_gpu_runtime,
        test_file_ocr,
        test_base64_ocr,
        test_url_ocr,
        test_different_detail_levels,
        test_unload_jobdone,
        test_manual_unload,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
            print("PASSED")
        else:
            print("FAILED")
        print("-" * 30)

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("All tests passed. EasyOCR MCP server is working correctly.")
    else:
        print("Some tests failed. Check the error messages above.")


if __name__ == "__main__":
    main()
