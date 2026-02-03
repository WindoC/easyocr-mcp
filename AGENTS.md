# AGENTS.md — easyocr-mcp

This repository contains an MCP (Model Context Protocol) server that provides OCR using EasyOCR. Details below mirror what exists in this repo and its README.

## Scope
- Applies to this repository rooted here.

## Overview
- Name: EasyOCR MCP Server
- Purpose: Provide OCR tools via EasyOCR for images (base64, file, URL).
- Entry point: `easyocr-mcp.py`

## Current Files (key)
- `easyocr-mcp.py` — MCP server and OCR tools.
- `README.md` — Features, install, usage, configuration, examples.
- `pyproject.toml` — Project metadata and dependencies.
- `test.py`, `test-gpu.py`, `test_mcp_tools.py` — Local test scripts.
- `test.png` — Sample image.
- `LICENSE`, `.gitignore`, `uv.lock`, `plan.md` — Licensing, ignores, lockfile, notes.

## Tools (as implemented)
- `ocr_image_base64` — OCR from base64-encoded image.
- `ocr_image_file` — OCR from an image file path.
- `ocr_image_url` — OCR from an image URL.

## Configuration
- Environment: `EASYOCR_LANGUAGES` — comma-separated language codes (default `en`).

## Install & Run (see README for details)
- Optional GPU (PyTorch): see README for the exact `uv pip install ...` command.
- Install deps and run:
  - `uv sync`
  - `uv run easyocr-mcp.py`
  - Example tests: `uv run test.py`, `uv run test-gpu.py`

## MCP Client Config
- See README section “MCP Configuration Example” for Windows and Linux/macOS JSON snippets.

