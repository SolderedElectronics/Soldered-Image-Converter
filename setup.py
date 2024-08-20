# Build script using cx_freeze
# This script is automatically ran with the build.ps1 script

from cx_Freeze import setup, Executable
import os

# Retrieve the version number from your version.py or another source
version = "v1.0.0"

# Executable name with the version number
executable_name = f"Soldered Image Converter {version}.exe"

# Build options, including icon and other files
build_exe_options = {
    "packages": ["os", "PySide6"],
    "include_files": [
        ("img/icon.ico", "icon.ico"),  # Ensures the icon is included
        ("img", "img"),  # Include the img directory
        ("test_images", "test_images"),
        "imageConverter.ui",
        "LICENSE",
    ],
    "include_msvcr": True,
}

# Define the executable, including the icon
executables = [
    Executable(
        "main.py",
        base="Win32GUI",  # Use Win32GUI for a Windows application without a console
        target_name=executable_name,
        icon="img/icon.ico",  # Set the executable icon
    )
]

# Setup call to package the application
setup(
    name="Soldered Image Converter",
    version=version,
    description="Soldered Image Converter is a desktop application which converts .png, .jpg, or .bmp format pictures (up to 10 at a time) to C++ compatible Arduino/Dasduino code, which you can use for your Soldered Displays.",
    options={"build_exe": build_exe_options},
    executables=executables,
)
