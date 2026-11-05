@echo off
title PPO Trained Robot Demo
pushd "%~dp0"

echo ==============================================================
echo   PPO Trained Robot Arm - 5,000,000 Steps 0%% Failure
echo ==============================================================
echo.
echo Loading trained model...
echo.
echo Controls:
echo   Mouse Left Drag  - Rotate camera
echo   Mouse Right Drag - Pan camera
echo   Mouse Wheel      - Zoom
echo   Close window     - Exit
echo.

cd /d "%~dp0embodied-intelligence"
python demo_trained_agent.py

echo.
echo Demo exited.
pause
