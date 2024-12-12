

# Define the Python version to install
$pythonVersion = "3.11.5"
$pythonInstallerUrl = "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion-amd64.exe"

# Define the installation path
$installPath = "C:\Python$pythonVersion"

# Download the installer
Write-Host "Downloading Python $pythonVersion..."
$installerPath = "$env:TEMP\python-$pythonVersion-installer.exe"
Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $installerPath

# Install Python silently
Write-Host "Installing Python $pythonVersion..."
Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 TargetDir=$installPath" -Wait

# Verify installation
Write-Host "Verifying Python installation..."
if (Get-Command "python" -ErrorAction SilentlyContinue) {
    python --version
    Write-Host "Python installed successfully!"
} else {
    Write-Host "Python installation failed!"
}

# Verify pip installation
if (Get-Command "pip" -ErrorAction SilentlyContinue) {
    pip --version
    Write-Host "Pip installed successfully!"
} else {
    Write-Host "Pip installation failed!"
}

# Clean up the installer
Write-Host "Cleaning up..."
Remove-Item -Path $installerPath -Force

Write-Host "Python installation complete!"
