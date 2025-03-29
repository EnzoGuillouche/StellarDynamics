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
$vpythonInstalled = python -c "import vpython" 2>$null
if ($?) {
    $vpythonVersion = pip show vpython | Select-String "Version" | ForEach-Object { ($_ -split " ")[1] }
    Write-Output "VPython is already installed: $vpythonVersion"
} else {
    Write-Output "VPython is not installed. Installing VPython..."
    pip install vpython
}

Write-Output "Starting simulation..."
python Src/main.py