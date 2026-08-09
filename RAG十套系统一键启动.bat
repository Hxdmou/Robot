@echo off
setlocal enabledelayedexpansion

title RAG十套系统一键启动 v3.4
cls
pushd "%~dp0"

echo.
echo ==============================================================
echo.
echo           RAG十套系统一键启动 v3.4
echo.
echo ==============================================================
echo.
echo   系统列表：
echo.
echo   [1]  通用RAG智能问答系统        (端口 7861)
echo   [2]  法律知识问答系统           (端口 7869)
echo   [3]  教育知识问答系统           (端口 7870)
echo   [4]  医疗健康问答系统           (端口 7871)
echo   [5]  金融知识问答系统           (端口 7872)
echo   [6]  IT技术问答系统             (端口 7873)
echo   [7]  电商零售问答系统           (端口 7874)
echo   [8]  政务服务问答系统           (端口 7875)
echo   [9]  人力资源问答系统           (端口 7876)
echo   [10] 科研学术问答系统           (端口 7877)
echo.
echo   [11] 一键启动全部10套系统 + 自动打开浏览器
echo   [0]  退出
echo.
echo ==============================================================
echo.
echo   当前目录: %CD%
echo.

set /p choice=  请输入选项数字: 

if "%choice%"=="0" goto end
if "%choice%"=="" goto end

rem 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo 错误：未找到Python，请先安装Python！
    pause
    exit /b 1
)

if "%choice%"=="11" goto start_all

echo.
echo 正在启动选中的系统...
echo.

if "%choice%"=="1" (
    start "通用RAG" cmd /k "cd /d ""%~dp0"" && streamlit run run.py --server.port 7861 --server.headless true"
    set "url=http://localhost:7861"
    goto open_single
)
if "%choice%"=="2" (
    start "法律知识" cmd /k "cd /d ""%~dp0"" && streamlit run legal_qa.py --server.port 7869 --server.headless true"
    set "url=http://localhost:7869"
    goto open_single
)
if "%choice%"=="3" (
    start "教育知识" cmd /k "cd /d ""%~dp0"" && streamlit run education_qa.py --server.port 7870 --server.headless true"
    set "url=http://localhost:7870"
    goto open_single
)
if "%choice%"=="4" (
    start "医疗健康" cmd /k "cd /d ""%~dp0"" && streamlit run medical_qa.py --server.port 7871 --server.headless true"
    set "url=http://localhost:7871"
    goto open_single
)
if "%choice%"=="5" (
    start "金融知识" cmd /k "cd /d ""%~dp0"" && streamlit run finance_qa.py --server.port 7872 --server.headless true"
    set "url=http://localhost:7872"
    goto open_single
)
if "%choice%"=="6" (
    start "IT技术" cmd /k "cd /d ""%~dp0"" && streamlit run tech_qa.py --server.port 7873 --server.headless true"
    set "url=http://localhost:7873"
    goto open_single
)
if "%choice%"=="7" (
    start "电商零售" cmd /k "cd /d ""%~dp0"" && streamlit run e_commerce_qa.py --server.port 7874 --server.headless true"
    set "url=http://localhost:7874"
    goto open_single
)
if "%choice%"=="8" (
    start "政务服务" cmd /k "cd /d ""%~dp0"" && streamlit run government_qa.py --server.port 7875 --server.headless true"
    set "url=http://localhost:7875"
    goto open_single
)
if "%choice%"=="9" (
    start "人力资源" cmd /k "cd /d ""%~dp0"" && streamlit run hr_qa.py --server.port 7876 --server.headless true"
    set "url=http://localhost:7876"
    goto open_single
)
if "%choice%"=="10" (
    start "科研学术" cmd /k "cd /d ""%~dp0"" && streamlit run academic_qa.py --server.port 7877 --server.headless true"
    set "url=http://localhost:7877"
    goto open_single
)

echo.
echo 无效选项！
pause
goto end

:open_single
echo.
echo 等待服务启动（15秒）...
timeout /t 15 /nobreak >nul
echo 正在打开浏览器: !url!
start "" "!url!"
echo.
echo 完成！如有错误请查看弹出的黑色cmd窗口。
goto end

:start_all
echo.
echo 正在启动全部10套系统，请稍候...
echo.

echo   [1/10] 启动通用RAG智能问答系统 (端口 7861)...
start "通用RAG" cmd /k "cd /d ""%~dp0"" && streamlit run run.py --server.port 7861 --server.headless true"
timeout /t 3 /nobreak >nul

echo   [2/10] 启动法律知识问答系统 (端口 7869)...
start "法律知识" cmd /k "cd /d ""%~dp0"" && streamlit run legal_qa.py --server.port 7869 --server.headless true"
timeout /t 2 /nobreak >nul

echo   [3/10] 启动教育知识问答系统 (端口 7870)...
start "教育知识" cmd /k "cd /d ""%~dp0"" && streamlit run education_qa.py --server.port 7870 --server.headless true"
timeout /t 2 /nobreak >nul

echo   [4/10] 启动医疗健康问答系统 (端口 7871)...
start "医疗健康" cmd /k "cd /d ""%~dp0"" && streamlit run medical_qa.py --server.port 7871 --server.headless true"
timeout /t 2 /nobreak >nul

echo   [5/10] 启动金融知识问答系统 (端口 7872)...
start "金融知识" cmd /k "cd /d ""%~dp0"" && streamlit run finance_qa.py --server.port 7872 --server.headless true"
timeout /t 2 /nobreak >nul

echo   [6/10] 启动IT技术问答系统 (端口 7873)...
start "IT技术" cmd /k "cd /d ""%~dp0"" && streamlit run tech_qa.py --server.port 7873 --server.headless true"
timeout /t 2 /nobreak >nul

echo   [7/10] 启动电商零售问答系统 (端口 7874)...
start "电商零售" cmd /k "cd /d ""%~dp0"" && streamlit run e_commerce_qa.py --server.port 7874 --server.headless true"
timeout /t 2 /nobreak >nul

echo   [8/10] 启动政务服务问答系统 (端口 7875)...
start "政务服务" cmd /k "cd /d ""%~dp0"" && streamlit run government_qa.py --server.port 7875 --server.headless true"
timeout /t 2 /nobreak >nul

echo   [9/10] 启动人力资源问答系统 (端口 7876)...
start "人力资源" cmd /k "cd /d ""%~dp0"" && streamlit run hr_qa.py --server.port 7876 --server.headless true"
timeout /t 2 /nobreak >nul

echo   [10/10] 启动科研学术问答系统 (端口 7877)...
start "科研学术" cmd /k "cd /d ""%~dp0"" && streamlit run academic_qa.py --server.port 7877 --server.headless true"

echo.
echo 等待所有服务就绪（30秒）...
echo   如果某个系统显示错误，关闭对应窗口后重新运行本启动器即可。
echo.
timeout /t 30 /nobreak >nul

echo 正在打开所有浏览器标签页...
echo.
start "" "http://localhost:7861"
timeout /t 1 /nobreak >nul
start "" "http://localhost:7869"
timeout /t 1 /nobreak >nul
start "" "http://localhost:7870"
timeout /t 1 /nobreak >nul
start "" "http://localhost:7871"
timeout /t 1 /nobreak >nul
start "" "http://localhost:7872"
timeout /t 1 /nobreak >nul
start "" "http://localhost:7873"
timeout /t 1 /nobreak >nul
start "" "http://localhost:7874"
timeout /t 1 /nobreak >nul
start "" "http://localhost:7875"
timeout /t 1 /nobreak >nul
start "" "http://localhost:7876"
timeout /t 1 /nobreak >nul
start "" "http://localhost:7877"

echo.
echo ==============================================================
echo.
echo           全部10套系统已启动完成！
echo.
echo ==============================================================
echo.
echo   访问地址：
echo      [1]  通用RAG智能问答系统:    http://localhost:7861
echo      [2]  法律知识问答系统:       http://localhost:7869
echo      [3]  教育知识问答系统:       http://localhost:7870
echo      [4]  医疗健康问答系统:       http://localhost:7871
echo      [5]  金融知识问答系统:       http://localhost:7872
echo      [6]  IT技术问答系统:         http://localhost:7873
echo      [7]  电商零售问答系统:       http://localhost:7874
echo      [8]  政务服务问答系统:       http://localhost:7875
echo      [9]  人力资源问答系统:       http://localhost:7876
echo      [10] 科研学术问答系统:       http://localhost:7877
echo.
echo   提示：关闭对应黑色cmd窗口即可停止该系统。
echo   如果页面显示"拒绝连接"，请再等待10秒后刷新页面。
echo   系统已预置基础使用说明索引，您可以直接上传自己的文档添加到知识库。
echo.

:end
echo.
pause
popd
