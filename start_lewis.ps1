# LEWIS - Linux Environment Working Intelligence System
# PowerShell Script for Windows

# Set console colors and encoding
$Host.UI.RawUI.ForegroundColor = "White"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Show-Banner {
    Write-Host @"

    ██╗     ███████╗██╗    ██╗██╗███████╗
    ██║     ██╔════╝██║    ██║██║██╔════╝
    ██║     █████╗  ██║ █╗ ██║██║███████╗
    ██║     ██╔══╝  ██║███╗██║██║╚════██║
    ███████╗███████╗╚███╔███╔╝██║███████║
    ╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝╚══════╝

    Linux Environment Working Intelligence System
    ================================================

"@ -ForegroundColor Cyan
}

function Test-PythonInstallation {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Python detected: $pythonVersion" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
        Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Yellow
        return $false
    }
    return $false
}

function Test-FirstRun {
    if (-not (Test-Path "config\config.yaml")) {
        Write-Host "🔧 First time setup detected..." -ForegroundColor Yellow
        Write-Host "Running LEWIS setup..." -ForegroundColor Blue
        
        python setup.py
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Setup failed" -ForegroundColor Red
            Read-Host "Press Enter to continue"
            exit 1
        }
        Write-Host ""
    }
}

function Show-Menu {
    Write-Host "Choose an option:" -ForegroundColor Yellow
    Write-Host "1. 💬 Start LEWIS CLI"
    Write-Host "2. 🎤 Start LEWIS CLI with Voice"
    Write-Host "3. 🌐 Start LEWIS Web Server"
    Write-Host "4. ⚙️  Run Setup Again"
    Write-Host "5. 📊 Show System Status"
    Write-Host "6. 🚪 Exit"
    Write-Host ""
}

function Start-LewisCLI {
    Write-Host ""
    Write-Host "🚀 Starting LEWIS CLI..." -ForegroundColor Green
    python lewis.py --mode cli
}

function Start-LewisCLIWithVoice {
    Write-Host ""
    Write-Host "🎤 Starting LEWIS CLI with Voice Support..." -ForegroundColor Green
    python lewis.py --mode cli --voice
}

function Start-LewisServer {
    Write-Host ""
    Write-Host "🌐 Starting LEWIS Web Server..." -ForegroundColor Green
    Write-Host "Access LEWIS at: http://localhost:5000" -ForegroundColor Cyan
    python lewis.py --mode server
}

function Start-LewisSetup {
    Write-Host ""
    Write-Host "⚙️ Running LEWIS setup..." -ForegroundColor Blue
    python setup.py
}

function Show-SystemStatus {
    Write-Host ""
    Write-Host "📊 LEWIS System Status" -ForegroundColor Yellow
    Write-Host "=====================" -ForegroundColor Yellow
    
    # Check Python
    if (Test-PythonInstallation) {
        Write-Host "✅ Python: Available" -ForegroundColor Green
    } else {
        Write-Host "❌ Python: Not Available" -ForegroundColor Red
    }
    
    # Check configuration
    if (Test-Path "config\config.yaml") {
        Write-Host "✅ Configuration: Available" -ForegroundColor Green
    } else {
        Write-Host "❌ Configuration: Missing" -ForegroundColor Red
    }
    
    # Check directories
    $directories = @("logs", "data", "outputs", "temp", "models")
    foreach ($dir in $directories) {
        if (Test-Path $dir) {
            Write-Host "✅ Directory $dir`: Available" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Directory $dir`: Missing" -ForegroundColor Yellow
        }
    }
    
    Write-Host ""
    Read-Host "Press Enter to continue"
}

function Test-ExtensionSystem {
    Write-Host "🔌 Checking extension system..." -ForegroundColor Yellow
    
    # Check Flask dependencies
    try {
        python -c "import flask, flask_socketio" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Extension dependencies available" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Installing extension dependencies..." -ForegroundColor Yellow
            pip install flask flask-socketio
        }
    } catch {
        Write-Host "❌ Failed to check extension dependencies" -ForegroundColor Red
        return $false
    }
    
    # Check examples directory
    if (Test-Path "examples") {
        Write-Host "✅ Examples directory found" -ForegroundColor Green
        
        # Check specific extensions
        $extensions = @(
            @{Name="Network Security Extension"; Path="examples\network_security_extension\extension.py"},
            @{Name="Custom Interface Extension"; Path="examples\custom_interface_extension\extension.py"}
        )
        
        foreach ($ext in $extensions) {
            if (Test-Path $ext.Path) {
                Write-Host "✅ $($ext.Name) found" -ForegroundColor Green
            } else {
                Write-Host "❌ $($ext.Name) missing" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "❌ Examples directory not found" -ForegroundColor Red
        Write-Host "Extension system may not work properly" -ForegroundColor Yellow
        return $false
    }
    
    return $true
}

# Main script execution
Clear-Host
Show-Banner

# Check Python installation
if (-not (Test-PythonInstallation)) {
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if first run
Test-FirstRun

# Main menu loop
do {
    Show-Menu
    $choice = Read-Host "Enter your choice (1-6)"
    
    switch ($choice) {
        "1" { Start-LewisCLI }
        "2" { Start-LewisCLIWithVoice }
        "3" { Start-LewisServer }
        "4" { Start-LewisSetup }
        "5" { Show-SystemStatus }
        "6" { 
            Write-Host ""
            Write-Host "👋 Thank you for using LEWIS!" -ForegroundColor Cyan
            Write-Host "Stay secure! 🛡️" -ForegroundColor Green
            exit 0
        }
        default { 
            Write-Host "Invalid choice. Please try again." -ForegroundColor Red
        }
    }
} while ($true)
