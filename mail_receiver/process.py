"""Process one saved EML file."""

import sys
from pathlib import Path

from src.processor import process_eml


def main() -> None:
    """Process the EML file path given as the first command-line argument."""
    process_eml(Path(sys.argv[1]))


if __name__ == "__main__":
    main()
