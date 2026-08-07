@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" x64
echo INCLUDE=%INCLUDE%
echo LIB=%LIB%
echo PATH=%PATH%