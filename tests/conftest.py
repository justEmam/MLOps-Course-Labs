"""Pytest conftest to ensure repository root is on sys.path.

Some CI or test runners change the current working directory; adding
the project root to `sys.path` makes `import app` reliable.
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
