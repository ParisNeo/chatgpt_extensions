#!/bin/bash

echo "Checking for Python and venv..."

if ! command -v python &> /dev/null
then
    echo "Python not found, installing..."
    if command -v apt-get > /dev/null; then
        sudo apt-get update
        sudo apt-get -y install python3 python3-venv
    elif command -v yum > /dev/null; then
        sudo yum -y update
        sudo yum -y install python3 python3-venv
    elif command -v pacman > /dev/null; then
        sudo pacman -Syu --noconfirm python python-venv
    fi
fi

echo "Activating virtual environment..."

if [ -f "env/bin/activate" ]
then
    source env/bin/activate && {
        echo "Virtual environment found. Updating dependencies..."
        python -m pip install --upgrade pip || exit 1
        pip install torch torchvision torchaudio || exit 1
        pip install -r requirements.txt || exit 1
    }
else
    echo "Virtual environment not found, creating..."
    python -m venv env || exit 1
    source env/bin/activate && {
        pip install torch torchvision torchaudio || exit 1
        pip install -r requirements.txt || exit 1
    }
fi

echo "Initializing submodules..."
git submodule update --init --recursive || exit 1
echo "Submodules initialized successfully."

echo "Requirements installed successfully."
read -n 1 -s -r -p "Press any key to exit..."
