#!/usr/bin/env python3
"""
Wrapper script for the Nomenic CLI.

This script allows running the Nomenic CLI directly from the project root:
$ python src/nomenic_cli.py --help

It ensures the src directory is in the Python path and handles both 
absolute and relative imports correctly.
"""

import os
import sys
from pathlib import Path


def main():
    """Main entry point for the CLI wrapper."""
    # Get the absolute path to the project root
    file_dir = Path(__file__).parent
    project_root = file_dir.parent  # Up one level from src/
    
    # Add the project root to Python path to ensure imports work
    sys.path.insert(0, str(project_root))
    
    try:
        # First try to import using absolute imports (installed package)
        try:
            from nomenic.cli.main import main as cli_main
        except ImportError:
            # If that fails, try relative imports (development mode)
            # Makes src the current directory
            os.chdir(file_dir)
            from nomenic.cli.main import main as cli_main
        
        # Run the CLI main function with the provided arguments
        exit_code = cli_main(sys.argv[1:])
        sys.exit(exit_code)
    
    except ImportError as e:
        print(f"ERROR: Failed to import Nomenic CLI modules: {e}", file=sys.stderr)
        print("Make sure you're running this script from the project root:", file=sys.stderr)
        print("  python src/nomenic_cli.py [COMMAND]", file=sys.stderr)
        print("\nOr install the package first with:", file=sys.stderr)
        print("  pip install -e .", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 