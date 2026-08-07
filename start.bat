@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

set "PYTHON_PATH="
where python >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=1" %%i in ('where python') do (
        set "PYTHON_PATH=%%i"
        goto :found_python
    )
)

:found_python
if not defined PYTHON_PATH (
    echo [ERROR] Python not found in PATH
    pause
    exit /b 1
)

cd /d "f:\个人作品\具身智能"
!PYTHON_PATH! visualize_minimal.py
pause