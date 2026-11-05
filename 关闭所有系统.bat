@echo off
title Close All RAG Systems
cls

echo.
echo ==============================
echo    Close All RAG Systems
echo ==============================
echo.
echo Stopping all RAG QA systems...
echo.

taskkill /f /im python.exe /t >nul 2>&1
taskkill /f /im streamlit.exe /t >nul 2>&1

echo.
echo All systems stopped!
echo.
pause
