@echo off
echo Building StartLoader Bootloader...
python scripts/build.py
if %errorlevel% neq 0 (
    echo.
    echo Build failed. Please ensure Python and the GNU toolchain (MinGW) are installed and in your PATH.
    pause
    exit /b %errorlevel%
)
echo.
echo Build successful!
pause
