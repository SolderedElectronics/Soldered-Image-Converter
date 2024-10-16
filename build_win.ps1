# Prompt for version number
$version = Read-Host "Enter the version number (e.g., 1.0.2)"

# Update version.py with the new version number
(Get-Content version.py) -replace 'version = "v.*"', "version = `"v$version`"" | Set-Content version.py

# Replace dots with underscores in the version number for folder naming
$versionUnderscore = $version -replace '\.', '_'

# Define the build path with the new folder name
$buildFolderName = "Soldered_Image_Converter_v${versionUnderscore}_win"
$buildPath = Join-Path "build" $buildFolderName

$exeName = "Soldered Image Converter.exe"

# Let's activate the venv
# Get the full path to the directory where this script is located
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Construct the path to the virtual environment's activation script
$venvActivationScript = Join-Path $scriptPath 'venv\Scripts\Activate.ps1'

# Check if the activation script exists
if (Test-Path $venvActivationScript) {
    # Dot-source the activation script to activate the virtual environment in the current shell
    . $venvActivationScript
    Write-Host "Virtual environment activated."
} else {
    Write-Host "Activation script not found at: $venvActivationScript"
}

# Check if the build folder already exists
if (Test-Path $buildPath) {
    $response = Read-Host "The build folder already exists. This will delete the existing build. Continue? (Y/N)"
    if ($response -match '^[Yy]$') {
        # Delete the existing build folder
        Remove-Item -Path $buildPath -Recurse -Force
    } else {
        Write-Host "Build aborted."
        exit
    }
}

# Ensure the build directory exists
New-Item -ItemType Directory -Force -Path $buildPath

# Remove existing spec file and PyInstaller cache if any
Remove-Item "main.spec" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force ".\__pycache__" -ErrorAction SilentlyContinue

# Resolve the absolute path to the icon file
$iconPath = (Resolve-Path ".\img\icon.ico").Path

# Resolve the absolute path to the font file
$fontPath = (Resolve-Path ".\source-sans-pro.ttf").Path

# Compile main.py using PyInstaller with the onefile flag, no console window, and set the icon
pyinstaller main.py `
    --onefile `
    --windowed `
    --noconsole `
    --clean `
    --icon="$iconPath" `
    --name "$exeName" `
    --add-data "$fontPath;." `
    --hidden-import=PySide6 `
    --distpath $buildPath

# Copy the specified folders to the build path
Copy-Item -Path .\img -Destination $buildPath -Recurse -Force
Copy-Item -Path .\test_images -Destination $buildPath -Recurse -Force

# Copy the specified files to the build path
$filesToCopy = @("imageConverter.ui", "LICENSE", "preview.png", "README.md")
foreach ($file in $filesToCopy) {
    Copy-Item -Path ".\$file" -Destination $buildPath -Force
}

# Create a ZIP archive of the build folder
$zipPath = Join-Path "build" "${buildFolderName}.zip"
if (Test-Path $zipPath) {
    Remove-Item -Path $zipPath -Force
}
Compress-Archive -Path $buildPath\* -DestinationPath $zipPath

Write-Host "Build and packaging complete. ZIP file created at $zipPath."
