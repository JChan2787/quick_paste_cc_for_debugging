@echo off

echo.
echo ============================================
echo    QuickPaste Debug Interface
echo ============================================
echo.

REM Navigate to quick_paste directory
cd quick_paste

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b
)

REM Check if dependencies are installed
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
    echo.
)

echo Starting server...
echo.

REM Open browser after a delay
start /b cmd /c "timeout /t 2 >nul && rundll32 url.dll,FileProtocolHandler http://localhost:8000/"

echo.
echo ============================================
echo    Server is running!
echo    
echo    URL: http://localhost:8000/
echo    
echo    Works with ALL browsers
echo    Files save to data/to-be-scanned/
echo    
echo    Keep this window open!
echo    Press Ctrl+C to stop the server
echo ============================================
echo.

REM Run the Node.js server
node server.js