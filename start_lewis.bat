@echo off
REM LEWIS - Linux Environment Working Intelligence System
REM Windows Batch Script for Easy Execution

echo.
echo    ██╗     ███████╗██╗    ██╗██╗███████╗
echo    ██║     ██╔════╝██║    ██║██║██╔════╝
echo    ██║     █████╗  ██║ █╗ ██║██║███████╗
echo    ██║     ██╔══╝  ██║███╗██║██║╚════██║
echo    ███████╗███████╗╚███╔███╔╝██║███████║
echo    ╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝╚══════╝
echo.
echo    Linux Environment Working Intelligence System
echo    ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if this is first run
if not exist "config\config.yaml" (
    echo 🔧 First time setup detected...
    echo Running LEWIS setup...
    python setup.py
    if %errorlevel% neq 0 (
        echo ❌ Setup failed
        pause
        exit /b 1
    )
    echo.
)

REM Check extension dependencies
echo 🔌 Checking extension system...
python -c "import flask, flask_socketio" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Extension dependencies missing - installing...
    pip install flask flask-socketio
)

REM Validate examples directory
if not exist "examples\" (
    echo ❌ Examples directory not found
    echo Extension system may not work properly
    pause
)

REM Check example extensions
if exist "examples\network_security_extension\extension.py" (
    echo ✅ Network Security Extension found
) else (
    echo ❌ Network Security Extension missing
)

if exist "examples\custom_interface_extension\extension.py" (
    echo ✅ Custom Interface Extension found
) else (
    echo ❌ Custom Interface Extension missing
)

REM Show menu
:menu
echo Choose an option:
echo 1. Start LEWIS CLI
echo 2. Start LEWIS CLI with Voice
echo 3. Start LEWIS Web Server
echo 4. Run Setup Again
echo 5. Show System Status
echo 6. Exit
echo.
set /p choice=Enter your choice (1-6): 

if "%choice%"=="1" goto cli
if "%choice%"=="2" goto cli_voice
if "%choice%"=="3" goto server
if "%choice%"=="4" goto setup
if "%choice%"=="5" goto status
if "%choice%"=="6" goto exit
echo Invalid choice. Please try again.
goto menu

:cli
echo.
echo 🚀 Starting LEWIS CLI...
python lewis.py --mode cli
goto menu

:cli_voice
echo.
echo 🎤 Starting LEWIS CLI with Voice Support...
python lewis.py --mode cli --voice
goto menu

:server
echo.
echo 🌐 Starting LEWIS Web Server...
echo Access LEWIS at: http://localhost:5000
python lewis.py --mode server
goto menu

:setup
echo.
echo ⚙️ Running LEWIS setup...
python setup.py
goto menu

:status
echo.
echo 📊 LEWIS System Status
echo =====================
python lewis.py --mode cli --help
goto menu

:exit
echo.
echo 👋 Thank you for using LEWIS!
echo Stay secure! 🛡️
pause
exit /b 0
