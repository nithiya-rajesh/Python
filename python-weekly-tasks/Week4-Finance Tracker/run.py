#!/usr/bin/env python3
"""
ENTRY POINT - Finance Tracker Application
==========================================

This script is the entry point for running the Finance Tracker.
It imports and runs the main application.

How to run:
    python run.py
"""

import sys
import os

# Add the project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run main
from finance_tracker.main import main

if __name__ == "__main__":
    main()
