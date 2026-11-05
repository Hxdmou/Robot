@echo off
title PyBullet Robot Simulation
pushd "%~dp0"

echo ==============================================================
echo           PyBullet Robot Arm Simulation
echo ==============================================================
echo.
echo Starting PyBullet 3D window...
echo.
echo Controls:
echo   Mouse Left Drag  - Rotate camera
echo   Mouse Right Drag - Pan camera
echo   Mouse Wheel      - Zoom
echo   Close window     - Exit
echo.

cd /d "%~dp0embodied-intelligence"
python pybullet_simulation.py

echo.
echo Simulation exited.
pause
