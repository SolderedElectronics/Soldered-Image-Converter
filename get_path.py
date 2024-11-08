# get_path.py

import os
import sys

def get_path(*path_segments):
    """
    Returns the absolute path to the directory where the main script is being executed from.
    If additional path segments are provided, they are appended to the base path.

    Parameters:
        *path_segments: Optional relative path segments to append to the base path.

    Returns:
        str: The absolute path.
    """
    if getattr(sys, 'frozen', False):
        # Running as a PyInstaller executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as a regular Python script
        try:
            base_path = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
        except AttributeError:
            # If '__main__' does not have a '__file__' attribute (e.g., in interactive mode),
            # default to the current working directory
            base_path = os.getcwd()

    # Combine the base path with any additional path segments
    return os.path.abspath(os.path.join(base_path, *path_segments))
