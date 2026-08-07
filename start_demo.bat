@echo off
chcp 65001 >nul 2>&1
title Robot Arm Ollama Control

echo ============================================
echo   Robot Arm Ollama Smart Control
echo ============================================
echo.
echo Starting robot arm GUI...
echo.

set "BASE=%~dp0"
cd /d "%BASE%"

python demo_robot_gui.py

echo.
echo Program exited. Press any key to close...
pause >nul