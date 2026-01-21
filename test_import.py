#!/usr/bin/env python3
"""Test script to verify backend.app can be imported"""

try:
    print("Attempting to import backend.app...")
    from backend.app import app
    print("✓ Successfully imported backend.app")
    print(f"✓ App object: {app}")
    print(f"✓ App name: {app.name}")
except Exception as e:
    print(f"✗ Error importing backend.app: {e}")
    import traceback
    traceback.print_exc()
