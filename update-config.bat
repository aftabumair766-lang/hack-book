@echo off
REM Helper script to update docusaurus.config.js with your GitHub username

echo ================================================
echo   Update Docusaurus Config for Deployment
echo ================================================
echo.

if "%1"=="" (
    echo Usage: update-config.bat YOUR_GITHUB_USERNAME
    echo.
    echo Example: update-config.bat johndoe
    echo.
    exit /b 1
)

set GITHUB_USER=%1

echo Updating docusaurus.config.js...
echo GitHub Username: %GITHUB_USER%
echo.

REM Create backup
copy docusaurus.config.js docusaurus.config.js.backup >nul
echo [OK] Created backup: docusaurus.config.js.backup

REM Replace YOUR_USERNAME with actual username (Windows compatible)
powershell -Command "(Get-Content docusaurus.config.js) -replace 'YOUR_USERNAME', '%GITHUB_USER%' | Set-Content docusaurus.config.js"

echo [OK] Configuration updated!

echo.
echo ================================================
echo   Configuration Updated Successfully!
echo ================================================
echo.
echo Your site will be:
echo   https://%GITHUB_USER%.github.io/hack_book/
echo.
echo Next steps:
echo   1. Create GitHub repo: https://github.com/new
echo   2. Repository name: hack_book
echo   3. Make it Public
echo   4. Run: git remote add origin https://github.com/%GITHUB_USER%/hack_book.git
echo   5. Run: git push -u origin main
echo   6. Run: npm run deploy
echo.
pause
