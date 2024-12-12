1. # Define repository URL and target directory:
$repoUrl = "https://github.com/JohnBummit/Twitter_Song_DB.git"
$targetDir = "Twitter_Song_DB"

# Function to clone the repository
function Clone-Repo {
    Write-Host "Cloning the repository..." -ForegroundColor Cyan
    git clone $repoUrl $targetDir
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Repository cloned successfully." -ForegroundColor Green
    } else {
        $errorMessage = $Error[0].ToString()
        if ($errorMessage -like "*already exists and is not an empty directory*") {
            Write-Host "Directory already exists. Checking status..." -ForegroundColor Yellow
            # Navigate to the directory and pull the latest changes
            cd $targetDir
            git pull origin main
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Repository updated successfully." -ForegroundColor Green
            } else {
                Write-Host "Failed to update repository. Please check the directory." -ForegroundColor Red
            }
        } else {
            Write-Host "An error occurred: $errorMessage" -ForegroundColor Red
        }
    }
}

# Check if the target directory exists
if (Test-Path $targetDir) {
    Write-Host "Directory $targetDir already exists. Attempting to update it..."
    cd $targetDir
    git pull origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Repository updated successfully." -ForegroundColor Green
    } else {
        Write-Host "Failed to update repository. Please check the directory." -ForegroundColor Red
    }
} else {
    # Clone the repository if the directory doesn't exist
    Clone-Repo
}
