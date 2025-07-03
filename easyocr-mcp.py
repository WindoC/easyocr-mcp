import os
import base64
import io
import requests
from PIL import Image as PILImage
from mcp.server.fastmcp import FastMCP
import easyocr

# Create an MCP server
mcp = FastMCP("EasyOCR")

# Reader cache for performance optimization
_reader_cache = {}

# Get default languages from environment variable
def get_default_languages() -> list[str]:
    """Get default languages from EASYOCR_LANGUAGES environment variable."""
    env_languages = os.getenv('EASYOCR_LANGUAGES', 'en')
    return [lang.strip() for lang in env_languages.split(',')]

def get_reader(languages: list[str]) -> easyocr.Reader:
    """
    Get or create an EasyOCR reader for the specified languages.
    Uses caching to avoid recreating readers for the same language combinations.
    """
    # Create a cache key from sorted languages
    cache_key = tuple(sorted(languages))
    
    if cache_key not in _reader_cache:
        try:
            # Create new reader - GPU usage determined at installation time
            _reader_cache[cache_key] = easyocr.Reader(languages)
        except Exception as e:
            raise ValueError(f"Failed to create EasyOCR reader for languages {languages}: {str(e)}")
    
    return _reader_cache[cache_key]

def validate_image_bytes(image_bytes: bytes) -> None:
    """
    Validate image bytes using PIL to ensure the image is valid and supported.
    """
    image_stream = io.BytesIO(image_bytes)
    try:
        pil_image = PILImage.open(image_stream)
        
        # Check if the format is supported
        if pil_image.format is None:
            raise ValueError("Unable to determine image format")
            
        # Verify the image can be loaded
        pil_image.verify()
        
    except (PILImage.UnidentifiedImageError, OSError) as e:
        raise ValueError(f"Invalid or unsupported image format: {e}")

@mcp.tool(title="OCR Image from Base64")
def ocr_image_base64(
    base64_image: str,
    detail: int = 1,
    paragraph: bool = False,
    width_ths: float = 0.7,
    height_ths: float = 0.7
) -> list:
    """
    Performs OCR on a base64 encoded image using EasyOCR.
    
    Args:
        base64_image: Base64 encoded image string
        detail: 0 for text only, 1 for full details with coordinates and confidence
        paragraph: Enable paragraph detection
        width_ths: Text width threshold for merging
        height_ths: Text height threshold for merging
    
    Returns:
        EasyOCR native output format:
        - detail=1: [([[x1,y1], [x2,y2], [x3,y3], [x4,y4]], 'text', confidence), ...]
        - detail=0: ['text1', 'text2', ...]
    """
    try:
        # Decode the base64 image string
        try:
            image_bytes = base64.b64decode(base64_image, validate=True)
        except base64.binascii.Error as e:
            raise ValueError(f"Invalid base64 string: {e}")

        # Validate image format
        validate_image_bytes(image_bytes)

        # Get EasyOCR reader for languages from environment
        languages = get_default_languages()
        reader = get_reader(languages)

        # Convert bytes to numpy array for EasyOCR
        import numpy as np
        from PIL import Image as PILImage
        
        image_stream = io.BytesIO(image_bytes)
        pil_image = PILImage.open(image_stream)
        
        # Convert PIL image to numpy array (RGB format)
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        image_array = np.array(pil_image)
        
        # Perform OCR using EasyOCR
        result = reader.readtext(
            image_array,
            detail=detail,
            paragraph=paragraph,
            width_ths=width_ths,
            height_ths=height_ths
        )

        return result

    except Exception as e:
        raise ValueError(f"Error performing OCR: {str(e)}")


@mcp.tool(title="OCR Image from File")
def ocr_image_file(
    image_path: str,
    detail: int = 1,
    paragraph: bool = False,
    width_ths: float = 0.7,
    height_ths: float = 0.7
) -> list:
    """
    Performs OCR on an image file using EasyOCR.
    
    Args:
        image_path: Path to the image file (full path)
        detail: 0 for text only, 1 for full details with coordinates and confidence
        paragraph: Enable paragraph detection
        width_ths: Text width threshold for merging
        height_ths: Text height threshold for merging
    
    Returns:
        EasyOCR native output format:
        - detail=1: [([[x1,y1], [x2,y2], [x3,y3], [x4,y4]], 'text', confidence), ...]
        - detail=0: ['text1', 'text2', ...]
    """
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"The file '{image_path}' was not found.")

        # Read image file
        with open(image_path, "rb") as file:
            image_bytes = file.read()

        # Validate image format
        validate_image_bytes(image_bytes)

        # Get EasyOCR reader for languages from environment
        languages = get_default_languages()
        reader = get_reader(languages)

        # Perform OCR directly on file path (EasyOCR can handle file paths)
        result = reader.readtext(
            image_path,
            detail=detail,
            paragraph=paragraph,
            width_ths=width_ths,
            height_ths=height_ths
        )

        return result
    
    except FileNotFoundError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError(f"Error performing OCR: {str(e)}")


@mcp.tool(title="OCR Image from URL")
def ocr_image_url(
    image_url: str,
    detail: int = 1,
    paragraph: bool = False,
    width_ths: float = 0.7,
    height_ths: float = 0.7
) -> list:
    """
    Performs OCR on an image from a URL using EasyOCR.
    
    Args:
        image_url: URL of the image to process
        detail: 0 for text only, 1 for full details with coordinates and confidence
        paragraph: Enable paragraph detection
        width_ths: Text width threshold for merging
        height_ths: Text height threshold for merging
    
    Returns:
        EasyOCR native output format:
        - detail=1: [([[x1,y1], [x2,y2], [x3,y3], [x4,y4]], 'text', confidence), ...]
        - detail=0: ['text1', 'text2', ...]
    """
    try:
        # Download image from URL
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            image_bytes = response.content
        except requests.RequestException as e:
            raise ValueError(f"Failed to download image from URL: {str(e)}")

        # Validate image format
        validate_image_bytes(image_bytes)

        # Get EasyOCR reader for languages from environment
        languages = get_default_languages()
        reader = get_reader(languages)

        # Convert bytes to numpy array for EasyOCR
        import numpy as np
        
        image_stream = io.BytesIO(image_bytes)
        pil_image = PILImage.open(image_stream)
        
        # Convert PIL image to numpy array (RGB format)
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        image_array = np.array(pil_image)
        
        # Perform OCR using EasyOCR
        result = reader.readtext(
            image_array,
            detail=detail,
            paragraph=paragraph,
            width_ths=width_ths,
            height_ths=height_ths
        )

        return result

    except Exception as e:
        raise ValueError(f"Error performing OCR: {str(e)}")

if __name__ == "__main__":
    mcp.run()
