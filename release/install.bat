@ECHO OFF
SETLOCAL

cd /d "%~dp0"

echo Installing PNFL...
echo.

py -m pip install --find-links packages pnfl
if %ERRORLEVEL% NEQ 0 goto :error

echo.
echo ============================================
echo   Installation Successful!
echo ============================================
echo.
echo The 'pnfl' command is now available from any terminal.
echo.
echo Usage:
echo   pnfl --help                  list available commands
echo   pnfl ^<command^> --help        show help for a specific command
echo.
echo See README.txt in this folder for instructions and examples
echo on how to run each tool.
echo.
echo The .bat files in this folder (convert-pdb.bat, etc.) are example
echo launchers you can edit and double-click instead of using a terminal.
echo ============================================
echo.
pause
exit /b 0

:error
echo.
echo ERROR: Installation failed. See above for details.
pause
exit /b 1
