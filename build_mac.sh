#!/bin/bash

# Prompt for version number
read -p "Enter the version number (e.g., 1.0.2): " version

# Update version.py with the new version number
sed -i '' "s/version = \"v.*\"/version = \"v$version\"/" version.py

# Replace dots with underscores in the version number for folder naming
versionUnderscore=${version//./_}

# Define the build path with the new folder name
buildFolderName="Soldered_Image_Converter_v${versionUnderscore}_mac"
buildPath="build/$buildFolderName"

exeName="Soldered Image Converter"

# Check if the venv folder exists and is in macOS-compatible format
venvFolder="venv"

if [ ! -d "$venvFolder" ] || [ -d "$venvFolder/Scripts" ]; then
    echo "Creating a new virtual environment."
    rm -rf "$venvFolder"  # Delete any existing incompatible venv
    python3 -m venv "$venvFolder"
fi

# Activate the virtual environment
venvActivationScript="$venvFolder/bin/activate"

if [ -f "$venvActivationScript" ]; then
    source "$venvActivationScript"
    echo "Virtual environment activated."
    
    # Install dependencies from requirements.txt
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo "requirements.txt not found. Please ensure dependencies are installed manually."
        exit 1
    fi
else
    echo "Activation script not found at: $venvActivationScript"
    exit 1
fi

# Check if the build folder already exists
if [ -d "$buildPath" ]; then
    read -p "The build folder already exists. This will delete the existing build. Continue? (Y/N): " response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        # Delete the existing build folder
        rm -rf "$buildPath"
    else
        echo "Build aborted."
        exit 1
    fi
fi

# Create the build directory
mkdir -p "$buildPath"

# Remove existing spec file and PyInstaller cache if any
rm -f main.spec
rm -rf __pycache__

# Resolve the absolute path to the icon file
iconPath=$(realpath "./img/icon.icns")

# Resolve the absolute path to the font file
fontPath=$(realpath "./source-sans-pro.ttf")

# Compile main.py using PyInstaller with the onefile flag, no console window, and set the icon
pyinstaller main.py \
    --onefile \
    --windowed \
    --noconsole \
    --clean \
    --icon="$iconPath" \
    --name "$exeName" \
    --add-data "$fontPath:." \
    --hidden-import=PySide6 \
    --distpath "$buildPath"

# Copy the specified folders to the build path
cp -R ./img "$buildPath"
cp -R ./test_images "$buildPath"

# Copy the specified files to the build path
filesToCopy=("imageConverter.ui" "LICENSE" "preview.png" "README.md")
for file in "${filesToCopy[@]}"; do
    cp "$file" "$buildPath"
done

# Create a ZIP archive of the build folder
zipPath="build/${buildFolderName}.zip"
if [ -f "$zipPath" ]; then
    rm -f "$zipPath"
fi
zip -r "$zipPath" "$buildPath"

echo "Build and packaging complete. ZIP file created at $zipPath."
