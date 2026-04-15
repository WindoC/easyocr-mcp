import sys

import easyocr
import torch


def main():
    print(f"python={sys.executable}")
    print(f"torch={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")
    print(f"hip_version={getattr(torch.version, 'hip', None)}")

    reader = easyocr.Reader(["en"])
    result = reader.readtext("test.png")
    print(result)


if __name__ == "__main__":
    main()
