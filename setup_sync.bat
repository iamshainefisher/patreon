@echo off
rem One-time setup: double-click this file.
cd /d "%~dp0"
echo Removing __pycache__ from GitHub (your local copy is kept)...
git rm -r --cached --ignore-unmatch -q __pycache__
echo Registering hourly sync task...
schtasks /create /tn "Sync Python Scripts" /tr "wscript.exe \"%~dp0sync_hidden.vbs\"" /sc hourly /f
echo Running first sync...
call sync.bat
type sync.log
echo.
echo Done. Close this window.
pause
