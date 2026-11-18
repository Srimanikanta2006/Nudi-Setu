"""Root entry point for Streamlit Community Cloud and local execution."""
import os
import sys
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parent
TARGET_APP = ROOT / "Last_Benchu_Party" / "problem_01" / "app.py"

# Ensure the target subfolder and project package are on sys.path
sys.path.insert(0, str(TARGET_APP.parent))

if __name__ == "__main__" or "streamlit" in sys.modules:
    runpy.run_path(str(TARGET_APP), run_name="__main__")
