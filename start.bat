@echo off
echo.
echo ============================================
echo   QuickPaste Debug Interface
echo ============================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

REM Check if dependencies are installed
if not exist node_modules (
    echo Installing dependencies...
    npm install
    echo.
)

echo Starting server...
echo.

REM Wait a moment before opening browser
timeout /t 2 /nobreak >nul

REM Open in default browser using rundll32 (properly respects Windows default)
echo Opening in your default browser...
rundll32 url.dll,FileProtocolHandler http://localhost:8000/

echo.
echo ============================================
echo   Server is running!
echo   
echo   URL: http://localhost:8000/
echo   
echo   ✅ Works with ALL browsers
echo   ✅ Files save to data\to-be-scanned\
echo   
echo   Keep this window open!
echo   Press Ctrl+C to stop the server
echo ============================================
echo.

REM Run the Node.js server
node server.js