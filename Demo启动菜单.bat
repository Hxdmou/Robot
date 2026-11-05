@echo off
title Embodied AI Demo Menu
pushd "%~dp0"

:menu
cls
echo.
echo ==============================================================
echo           Embodied AI Demo Menu v1.0
echo ==============================================================
echo.
echo   [1] Robot Arm GUI Demo
echo   [2] RAG 10 Systems (browser)
echo   [3] Deploy Health Check Demo
echo   [4] GUI Control Demo
echo   [5] Simulation Demo
echo   [0] Exit
echo.
echo ==============================================================
echo.
set /p choice=Select option: 

if "%choice%"=="1" goto robot
if "%choice%"=="2" goto rag
if "%choice%"=="3" goto health
if "%choice%"=="4" goto gui
if "%choice%"=="5" goto sim
if "%choice%"=="0" goto end
goto menu

:robot
call start_demo.bat
goto menu

:rag
call "RAG十套系统一键启动.bat"
goto menu

:health
cd /d "%~dp0_PUBLIC_NTA_OUTPUT\EmbodiedSim-Framework\examples"
python deploy_health_check_demo.py
pause
goto menu

:gui
cd /d "%~dp0_PUBLIC_NTA_OUTPUT\EmbodiedSim-Framework\examples"
python gui_control_demo.py
pause
goto menu

:sim
cd /d "%~dp0_PUBLIC_NTA_OUTPUT\EmbodiedSim-Framework\examples"
python run_simulation_demo.py
pause
goto menu

:end
exit
