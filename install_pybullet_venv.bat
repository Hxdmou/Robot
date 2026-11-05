@echo off
cd /d "f:\个人作品\具身智能"

echo Setting up Visual Studio environment...
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" x64

echo Installing pybullet...
env_pybullet\Scripts\pip.exe install pybullet

echo Done!
pause