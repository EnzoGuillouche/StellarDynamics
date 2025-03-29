clear

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Checking Python installation..."
if ! command_exists python3; then
    echo "Python is not installed. Installing Python..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"  # Install Homebrew if missing
    brew install python
else
    echo "Python is already installed: $(python3 --version)"
fi

echo "Checking VPython installation..."
if ! python3 -c "import vpython" 2>/dev/null; then
    echo "VPython is not installed. Installing VPython..."
    pip3 install vpython
else
    echo "VPython is already installed."
fi

echo "Starting simulation..."
python3 Src/main.py