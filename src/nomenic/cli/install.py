"""Installation script to set up the Nomenic CLI."""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def ensure_virtual_env():
    """Check if running in a virtual environment."""
    if not hasattr(sys, 'real_prefix') and not hasattr(sys, 'base_prefix'):
        print("WARNING: It's recommended to install Nomenic in a virtual environment.")
        choice = input("Continue anyway? [y/N]: ")
        if choice.lower() != 'y':
            print("Installation aborted.")
            sys.exit(0)


def check_pip():
    """Check if pip is available."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_package():
    """Install the package in development mode."""
    project_root = Path(__file__).parent.parent.parent.parent
    setup_py = project_root / "setup.py"
    
    if not setup_py.exists():
        print(f"ERROR: setup.py not found at {setup_py}")
        print("Make sure you're running this script from within the Nomenic project.")
        return False
    
    print("Installing Nomenic in development mode...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", str(project_root)])
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install package: {e}")
        return False


def create_test_script():
    """Create a test script to verify the installation."""
    test_script = Path.home() / "test_nomenic.py"
    
    content = """#!/usr/bin/env python3
import sys

try:
    import nomenic
    from nomenic.cli.main import main
    print(f"Nomenic version {nomenic.__version__} successfully installed!")
    print("Try running: nomenic --help")
    
    # Test the CLI
    sys.argv = ["nomenic", "--help"]
    main()
except ImportError as e:
    print(f"ERROR: Failed to import Nomenic modules: {e}")
    print("Make sure the package is properly installed.")
    sys.exit(1)
"""
    
    with open(test_script, "w") as f:
        f.write(content)
    
    # Make executable on Unix-like systems
    if os.name != "nt":  # not Windows
        mode = os.stat(test_script).st_mode
        os.chmod(test_script, mode | 0o111)  # Add execute permission
    
    return test_script


def verify_installation():
    """Verify that the installation worked."""
    try:
        # Check if the entry point is in PATH
        nomenic_path = shutil.which("nomenic")
        if nomenic_path:
            print(f"Nomenic CLI entry point found at: {nomenic_path}")
        else:
            print("WARNING: Nomenic CLI entry point not found in PATH.")
            print("You can still run the CLI using 'python -m nomenic.cli.main'")
        
        # Create and run test script
        test_script = create_test_script()
        print(f"\nCreated test script at: {test_script}")
        print(f"Run it with: {sys.executable} {test_script}")
        
        return True
    except Exception as e:
        print(f"ERROR during verification: {e}")
        return False


def main():
    """Main installation function."""
    print("Nomenic Installation Helper")
    print("==========================")
    
    # Check environment
    ensure_virtual_env()
    
    # Check for pip
    if not check_pip():
        print("ERROR: pip not found. Please make sure pip is installed and in your PATH.")
        sys.exit(1)
    
    # Install the package
    if install_package():
        print("\nNomenic installation completed!")
        
        # Verify installation
        if verify_installation():
            print("\nInstallation verified successfully!")
            print("\nYou can now use Nomenic from the command line with:")
            print("  nomenic --help")
            print("\nOr if the entry point is not in your PATH, you can run:")
            print(f"  {sys.executable} -m nomenic.cli.main --help")
            
            print("\nTo test with a sample file, run:")
            print("  nomenic validate <file>")
            print("  nomenic debug <file>")
            print("  nomenic render <file> --format html")
    else:
        print("\nInstallation failed. Please check the error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main() 