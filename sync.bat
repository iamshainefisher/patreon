@echo off
rem Keeps this folder and GitHub in sync. Run by Task Scheduler; log in sync.log
cd /d "%~dp0"
>>sync.log echo ==== %date% %time% ====
git pull --rebase --autostash >>sync.log 2>&1 || goto :fail
git add -A >>sync.log 2>&1
git diff --cached --quiet || git commit -m "Auto-sync %date% %time%" >>sync.log 2>&1
git push >>sync.log 2>&1 || goto :fail
>>sync.log echo OK
exit /b 0
:fail
>>sync.log echo FAILED - open this folder in GitHub Desktop or VS Code to sort it out
exit /b 1
