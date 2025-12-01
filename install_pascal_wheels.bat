@echo off
REM ============================================================================
REM Minimal Pascal Wheel Installer
REM Installs torch, torchvision, torchaudio wheels into a venv
REM -----------------------------------------------------------------------------
REM USAGE:
REM   install_pascal_wheels_only.bat <venv_path> [flags]
REM FLAGS:
REM   --torch        Install torch
REM   --torchvision  Install torchvision
REM   --torchaudio   Install torchaudio
REM   (any combination allowed)
REM   --help, --h    Show this help message
REM EXAMPLES:
REM   install_pascal_wheels_only.bat C:\path\to\venv --torch --torchvision
REM   install_pascal_wheels_only.bat C:\path\to\venv --torchaudio
REM   install_pascal_wheels_only.bat C:\path\to\venv --torch
REM -----------------------------------------------------------------------------
REM This script is intended to be called from setup.bat or manually.
REM ============================================================================

REM Show help if requested
if /i "%~1"=="--help" goto :show_help
if /i "%~1"=="--h" goto :show_help

setlocal EnableDelayedExpansion

REM Parse arguments
set "VENV_PATH="
set "INSTALL_TORCH=0"
set "INSTALL_TORCHVISION=0"
set "INSTALL_TORCHAUDIO=0"

if "%~1"=="" (
    echo ERROR: Missing venv path argument
    goto :show_help
)
set "VENV_PATH=%~1"
shift

:parse_flags
if "%~1"=="" goto :flags_done
if /i "%~1"=="--torch" (
    set "INSTALL_TORCH=1"
    shift
    goto :parse_flags
)
if /i "%~1"=="--torchvision" (
    set "INSTALL_TORCHVISION=1"
    shift
    goto :parse_flags
)
if /i "%~1"=="--torchaudio" (
    set "INSTALL_TORCHAUDIO=1"
    shift
    goto :parse_flags
)
shift
goto :parse_flags
:flags_done

set "PIP_EXE=%VENV_PATH%\Scripts\pip.exe"
set "SCRIPT_DIR=%~dp0..\wheels\"

REM If no install flags, print help and exit
if "%INSTALL_TORCH%"=="0" if "%INSTALL_TORCHVISION%"=="0" if "%INSTALL_TORCHAUDIO%"=="0" goto :show_help

REM Install torch if requested
if "%INSTALL_TORCH%"=="1" (
    for %%f in ("%SCRIPT_DIR%torch-*.whl") do (
        echo Installing torch: %%f
        "%PIP_EXE%" install "%%f"
    )
)

REM Install torchvision if requested
if "%INSTALL_TORCHVISION%"=="1" (
    for %%f in ("%SCRIPT_DIR%torchvision-*.whl") do (
        echo Installing torchvision: %%f
        "%PIP_EXE%" install "%%f"
    )
)

REM Install torchaudio if requested
if "%INSTALL_TORCHAUDIO%"=="1" (
    for %%f in ("%SCRIPT_DIR%torchaudio-*.whl") do (
        echo Installing torchaudio: %%f
        "%PIP_EXE%" install "%%f"
    )
)

echo Installation complete.
exit /b 0

:show_help
@echo ============================================================================
@echo Minimal Pascal Wheel Installer
@echo Installs torch, torchvision, torchaudio wheels into a venv
@echo -----------------------------------------------------------------------------
@echo USAGE:
@echo   install_pascal_wheels_only.bat ^<venv_path^> [flags]
@echo FLAGS:
@echo   --torch        Install torch
@echo   --torchvision  Install torchvision
@echo   --torchaudio   Install torchaudio
@echo   (any combination allowed)
@echo   --help, --h    Show this help message
@echo EXAMPLES:
@echo   install_pascal_wheels_only.bat C:\path\to\venv --torch --torchvision
@echo   install_pascal_wheels_only.bat C:\path\to\venv --torchaudio
@echo   install_pascal_wheels_only.bat C:\path\to\venv --torch
@echo -----------------------------------------------------------------------------
@echo This script is intended to be called from setup.bat or manually.
@echo ============================================================================
exit /b 0
