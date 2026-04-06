from pathlib import Path
import os

# 1. __file__ gets the path of security.py
# 2. .resolve() gets the absolute path
# 3. .parents[1] goes up two levels (out of 'utils', to 'RESRAG')
ROOT_DIR = Path(__file__).resolve().parents[1]

def is_safe_path(target_path_string):
    """Checks if a target path resolves to a location inside the ROOT_DIR."""
    try:
        target_path = Path(target_path_string).resolve()
        if ROOT_DIR not in target_path.parents and target_path != ROOT_DIR:
            return False
        return True
    except Exception:
        return False

def enforce_safe_path(target_path_string):
    """Raises an error if the path is outside the jail."""
    if not is_safe_path(target_path_string):
        raise PermissionError(f"Security Alert: Path traversal attempt blocked for '{target_path_string}'")