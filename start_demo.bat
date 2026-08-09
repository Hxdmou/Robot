@echo off
title Robot Arm Demo
pushd "%~dp0"

echo ==============================================================
echo           Robot Arm Intelligent Control Demo v1.0
echo ==============================================================
echo.

echo [1/3] Starting Ollama service if needed...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    start "" /B ollama serve
    timeout /t 6 /nobreak >nul
)

echo [2/3] Changing directory...
cd /d "%~dp0embodied-intelligence"

echo [3/3] Launching Robot GUI...
echo.
echo Mouse: Left=Rotate Right=Pan Wheel=Zoom
echo Keys: H=Home R=Reset C=ResetView ESC=Exit
echo.

python demo_robot_gui.py

echo.
echo Demo exited.
pause
