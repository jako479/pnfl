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
echo To get started:
echo   1. Edit the .bat file for the command you want to run
echo      (e.g. convert-pdb.bat) with your file paths
echo   2. Double-click the .bat file to run
echo.
echo See the .ini files in this folder for additional settings.
echo ============================================
echo.
pause
exit /b 0

:error
echo.
echo ERROR: Installation failed. See above for details.
pause
exit /b 1
