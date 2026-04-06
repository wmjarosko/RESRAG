from pathlib import Path
import os

# Define the absolute root of your project
ROOT_DIR = Path("D:/Repos/RESRAG").resolve()

def is_safe_path(target_path_string):
    """
    Checks if a target path resolves to a location inside the ROOT_DIR.
    """
    try:
        target_path = Path(target_path_string).resolve()
        if ROOT_DIR not in target_path.parents and target_path != ROOT_DIR:
            return False
        return True
    except Exception:
        return False

def enforce_safe_path(target_path_string):
    """
    Raises an error if the path is outside the jail.
    Use this right before running any open() or fitz.open() commands.
    """
    if not is_safe_path(target_path_string):
        raise PermissionError(f"Security Alert: Path traversal attempt blocked for '{target_path_string}'")