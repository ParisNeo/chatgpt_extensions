@echo off
call env\Scripts\activate.bat
python chatgpt_helper_service.py
if %errorlevel% neq 0 (
    echo An error occurred. Press any key to exit...
    pause > nul
)