cls

function Command-Exists {
    param ($cmd)
    return [bool](Get-Command $cmd -ErrorAction SilentlyContinue)
}

Write-Output "Checking Python installation..."
if (-not (Command-Exists "python")) {
    Write-Output "Python is not installed. Installing Python..."
    # Install Python using winget (Requires Windows 10/11)
    winget install Python.Python -e
} else {
    Write-Output "Python is already installed: $(python --version)"
}

Write-Output "Checking VPython installation..."
if (-not (python -c "import vpython" 2>$null)) {
    Write-Output "VPython is not installed. Installing VPython..."
    pip install vpython
} else {
    $vpythonVersion = pip show vpython | Select-String "Version" | ForEach-Object { ($_ -split " ")[1] }
    Write-Output "VPython is already installed: $vpythonVersion"
}

Write-Output "Starting simulation..."
python Src/main.py