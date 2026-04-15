import sys

import torch


def main():
    print(f"python={sys.executable}")
    print(f"torch={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")
    print(f"hip_version={getattr(torch.version, 'hip', None)}")
    print(f"cuda_version={torch.version.cuda}")

    if not torch.cuda.is_available():
        raise SystemExit("GPU runtime is not available")

    if not getattr(torch.version, "hip", None):
        raise SystemExit("Expected an AMD ROCm/HIP-enabled PyTorch build")

    print("GPU runtime check passed")


if __name__ == "__main__":
    main()
