# Define the URL for the Git installer
$gitDownloadUrl = "https://github.com/git-for-windows/git/releases/download/v2.45.2.windows.1/Git-2.45.2-64-bit.exe"

# Set the path to download the installer
$installerPath = "$env:TEMP\GitInstaller.exe"

# Download the Git installer
Write-Host "Downloading Git installer..." -ForegroundColor Cyan
Invoke-WebRequest -Uri $gitDownloadUrl -OutFile $installerPath -UseBasicParsing -Verbose

# Check if the installer was downloaded
if (Test-Path $installerPath) {
    Write-Host "Download complete. Installing Git..." -ForegroundColor Cyan
    # Run the installer silently
    Start-Process -FilePath $installerPath -ArgumentList "/SILENT" -Wait

    # Remove the installer file
    Remove-Item -Path $installerPath -Force
    Write-Host "Git installed successfully. Checking version..." -ForegroundColor Green
    git --version
} else {
    Write-Host "Download failed. Please check the URL or network connection." -ForegroundColor Red
}
