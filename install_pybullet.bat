@echo off
echo Setting up Visual Studio Build Tools environment...
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" x64
if %errorlevel% neq 0 (
    echo Failed to set up Visual Studio environment!
    pause
    exit /b 1
)
echo Adding Windows SDK paths...
set "INCLUDE=C:\Program Files (x86)\Windows Kits\10\Include\10.0.22621.0\ucrt;C:\Program Files (x86)\Windows Kits\10\Include\10.0.22621.0\shared;C:\Program Files (x86)\Windows Kits\10\Include\10.0.22621.0\um;C:\Program Files (x86)\Windows Kits\10\Include\10.0.22621.0\winrt;%INCLUDE%"
set "LIB=C:\Program Files (x86)\Windows Kits\10\Lib\10.0.22621.0\ucrt\x64;C:\Program Files (x86)\Windows Kits\10\Lib\10.0.22621.0\um\x64;%LIB%"
set "PATH=C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64;C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64;%PATH%"
echo Environment set up successfully.
echo Installing pybullet...
python -m pip install --user pybullet -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo Failed to install pybullet!
    pause
    exit /b 1
)
echo pybullet installed successfully!
python -c "import pybullet; print('pybullet imported successfully')"
pause