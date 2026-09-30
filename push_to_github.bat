@echo off
title Push kibo-PRC to GitHub
echo ============================================================
echo   Syncing kibo-PRC local commits to GitHub
echo   Repository: https://github.com/korbsameth/kibo-PRC
echo   Author: korb sameth
echo ============================================================
echo.
cd /d "%~dp0"
git push origin main
echo.
if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] Commits pushed successfully to GitHub!
) else (
    echo [ERROR] Push failed. Please check your GitHub credentials or internet connection.
)
echo.
pause
