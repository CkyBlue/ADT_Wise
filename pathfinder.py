"""Stackoverfow solution to making pyinstaller's onefile executable work with data bundling
Use the return as the path to be used"""

import os, sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
