# Define paths to the scripts
$pythonScriptPath = "./Twitter_Song_DB/for_new_ppl/install_python.ps1"
$gitScriptPath = "./Twitter_Song_DB/for_new_ppl/install_git.ps1"

# Function to check and run a script if it exists
function Run-ScriptIfExists {
    param (
        [string]$scriptPath,
        [string]$checkCommand,
        [string]$softwareName
    )

    # Check if the software is already installed
    try {
        & $checkCommand > $null 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Output "$softwareName is already installed. Skipping $scriptPath."
            return
        }
    } catch {
        Write-Output "$softwareName is not installed. Running the script..."
    }

    # Run the script if the software is not installed
    if (Test-Path $scriptPath) {
        try {
            & $scriptPath
            Write-Output "$softwareName installation script executed successfully."
        } catch {
            Write-Error "An error occurred while running '$scriptPath': $($_.Exception.Message)"
        }
    } else {
        Write-Error "Error: '$scriptPath' not found! Please verify the file location."
    }
}

# Check and install Python if necessary
Run-ScriptIfExists -scriptPath $pythonScriptPath -checkCommand "python --version" -softwareName "Python"

# Check and install Git if necessary
Run-ScriptIfExists -scriptPath $gitScriptPath -checkCommand "git --version" -softwareName "Git"

# Output completion message
Write-Output "All scripts have been processed. Check for any errors in the output above."
