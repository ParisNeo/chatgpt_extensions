@echo off
setlocal

echo Checking for Python and venv...
where python > nul 2>&1 || (
    echo Python not found. Please download and install Python from https://www.python.org/downloads/ and add it to the PATH.
    goto :error
)

echo Activating virtual environment...
if exist env\Scripts\activate.bat (
    call env\Scripts\activate.bat && (
        echo Virtual environment found. Updating dependencies...
        python -m pip install --upgrade pip || goto :error
        pip install torch torchvision torchaudio || goto :error
        pip install -r requirements.txt || goto :error
    )
) else (
    echo Virtual environment not found, creating...
    python -m venv env || goto :error
    call env\Scripts\activate.bat && (
        pip install torch torchvision torchaudio || goto :error
        pip install -r requirements.txt || goto :error
    )
)

echo Initializing submodules...
git submodule update --init --recursive || goto :error
echo Submodules initialized successfully.

echo Requirements installed successfully.
pause
goto :end

:error
echo An error occurred. Press any key to exit...
echo To run the application, just run run.bat.
pause > nul
pause

:end
