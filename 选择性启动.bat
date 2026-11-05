@echo off
setlocal enabledelayedexpansion

title RAG System Launcher
cls

echo.
echo ==============================
echo    RAG System Launcher v2.1
echo ==============================
echo.
echo Select system to start:
echo.
echo 1 - General RAG QA System (port 7861)
echo 2 - Legal QA System (port 7869)
echo 3 - Education QA System (port 7870)
echo 4 - Medical QA System (port 7871)
echo 5 - Finance QA System (port 7872)
echo 6 - Tech QA System (port 7873)
echo 7 - E-Commerce QA System (port 7874)
echo 8 - Government QA System (port 7875)
echo 9 - HR QA System (port 7876)
echo 10 - Academic QA System (port 7877)
echo.
echo 11 - Start All Systems
echo 0 - Exit
echo.
echo ==============================
echo.

set /p choice=Enter number:

if "%choice%"=="0" goto end

if "%choice%"=="11" goto start_all

if "%choice%"=="" (
    echo No input, exiting...
    goto end
)

echo.
echo Starting selected system...
echo.

if "%choice%"=="1" start "RAG General" cmd /k streamlit run run.py --server.port 7861 --server.headless true
if "%choice%"=="2" start "RAG Legal" cmd /k streamlit run legal_qa.py --server.port 7869 --server.headless true
if "%choice%"=="3" start "RAG Education" cmd /k streamlit run education_qa.py --server.port 7870 --server.headless true
if "%choice%"=="4" start "RAG Medical" cmd /k streamlit run medical_qa.py --server.port 7871 --server.headless true
if "%choice%"=="5" start "RAG Finance" cmd /k streamlit run finance_qa.py --server.port 7872 --server.headless true
if "%choice%"=="6" start "RAG Tech" cmd /k streamlit run tech_qa.py --server.port 7873 --server.headless true
if "%choice%"=="7" start "RAG E-Commerce" cmd /k streamlit run e_commerce_qa.py --server.port 7874 --server.headless true
if "%choice%"=="8" start "RAG Government" cmd /k streamlit run government_qa.py --server.port 7875 --server.headless true
if "%choice%"=="9" start "RAG HR" cmd /k streamlit run hr_qa.py --server.port 7876 --server.headless true
if "%choice%"=="10" start "RAG Academic" cmd /k streamlit run academic_qa.py --server.port 7877 --server.headless true

echo.
echo Done!
goto end

:start_all
echo Starting all systems...
echo.

start "RAG General" cmd /k streamlit run run.py --server.port 7861 --server.headless true
timeout /t 2 /nobreak >nul

start "RAG Legal" cmd /k streamlit run legal_qa.py --server.port 7869 --server.headless true
timeout /t 2 /nobreak >nul

start "RAG Education" cmd /k streamlit run education_qa.py --server.port 7870 --server.headless true
timeout /t 2 /nobreak >nul

start "RAG Medical" cmd /k streamlit run medical_qa.py --server.port 7871 --server.headless true
timeout /t 2 /nobreak >nul

start "RAG Finance" cmd /k streamlit run finance_qa.py --server.port 7872 --server.headless true
timeout /t 2 /nobreak >nul

start "RAG Tech" cmd /k streamlit run tech_qa.py --server.port 7873 --server.headless true
timeout /t 2 /nobreak >nul

start "RAG E-Commerce" cmd /k streamlit run e_commerce_qa.py --server.port 7874 --server.headless true
timeout /t 2 /nobreak >nul

start "RAG Government" cmd /k streamlit run government_qa.py --server.port 7875 --server.headless true
timeout /t 2 /nobreak >nul

start "RAG HR" cmd /k streamlit run hr_qa.py --server.port 7876 --server.headless true
timeout /t 2 /nobreak >nul

start "RAG Academic" cmd /k streamlit run academic_qa.py --server.port 7877 --server.headless true

echo All systems started!
goto end

:end
echo.
pause
