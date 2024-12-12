# Define Git version and download URL
$gitVersion = "2.42.0"
$gitInstallerUrl = "https://github.com/git-for-windows/git/releases/download/v$gitVersion.windows.1/Git-$gitVersion-64-bit.exe"

# Define temporary file path for the installer
$installerPath = "$env:TEMP\git-$gitVersion-installer.exe"

# Download the Git installer
Write-Host "Downloading Git version $gitVersion..."
Invoke-WebRequest -Uri $gitInstallerUrl -OutFile $installerPath

# Install Git silently
Write-Host "Installing Git version $gitVersion..."
Start-Process -FilePath $installerPath -ArgumentList "/VERYSILENT" -Wait

# Verify installation
Write-Host "Verifying Git installation..."
if (Get-Command "git" -ErrorAction SilentlyContinue) {
    git --version
    Write-Host "Git installed successfully!"
} else {
    Write-Host "Git installation failed!"
}

# Clean up the installer
Write-Host "Cleaning up..."
Remove-Item -Path $installerPath -Force

Write-Host "Git installation complete!"
