@echo off
cd /d "%~dp0"

python -c "import numpy; v = numpy.__version__.split('.'); exit(0 if int(v[0]) < 2 else 1)" 2>nul
if errorlevel 1 (
    echo [WARNING] NumPy version may be incompatible with PyBullet.
    echo Installing numpy^<2 ...
    pip install "numpy<2" -q
)

python kuka_lift.py
pause
