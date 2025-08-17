#!/usr/bin/env python3
"""
VidHarvester Application Entry Point

This script serves as the main entry point for the VidHarvester application.
It sets up the Python path to include the src directory and launches the app.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    from vidharvester.app import main
    main()
