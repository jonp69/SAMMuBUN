@echo off
REM ================================================
echo [1/4] Creating or activating virtual environment...
echo ================================================

REM Check if venv exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ERROR: Failed to activate venv
        pause
        exit /b 1
    )
    echo [INFO] Activated existing venv
) else (
    C:\Python311\python.exe -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create venv
        pause
        exit /b 1
    )
    call .venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ERROR: Failed to activate new venv
        pause
        exit /b 1
    )
    echo [INFO] Created and activated new venv
)

REM ================================================
echo [2/4] Installing packages from requirements.txt...
echo ================================================
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)
if exist requirements.txt (
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
) else (
    echo ERROR: requirements.txt not found
    pause
    exit /b 1
)

REM ================================================
echo [INFO] Installing Pascal wheels (torch, torchvision, torchaudio)...
call install_pascal_wheels.bat .venv --torch --torchvision --torchaudio
if errorlevel 1 (
    echo ERROR: Pascal wheels install failed
    pause
    exit /b 1
)

REM ================================================
echo [3/4] Running Video Meme Compositor...
echo ================================================
pause
python video_meme_compositor.py
if errorlevel 1 (
    echo ERROR: Application failed
    pause
    exit /b 1
)

REM ================================================
echo [4/4] Application closed!
echo ================================================
pause
exit /b 0
