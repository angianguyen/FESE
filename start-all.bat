@echo off
echo ========================================
echo StreamCredit - Full Stack Startup
echo ========================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js is not installed!
    echo Please download from: https://nodejs.org/
    pause
    exit /b 1
)

echo [1/3] Starting Mock API Server...
start "StreamCredit Mock API" cmd /k "cd mock-api && npm install && npm start"
timeout /t 3 /nobreak >nul

echo [2/3] Starting Frontend...
start "StreamCredit Frontend" cmd /k "cd frontend && npm install && npm run dev"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo ✅ All services started!
echo ========================================
echo.
echo 🌐 Frontend:  http://localhost:3000
echo 🔧 Mock API:  http://localhost:3001
echo.
echo Press any key to open browser...
pause >nul

start http://localhost:3000

echo.
echo Services are running in separate windows.
echo Close those windows to stop the servers.
echo.
pause
