# Birthday Email Scheduler - Setup Script
# Run this script to set up and start the Birthday Email Scheduler

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BIRTHDAY EMAIL SCHEDULER - SETUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check prerequisites
Write-Host "`n[1/6] Checking prerequisites..." -ForegroundColor Yellow

# Check Docker
try {
    $dockerVersion = docker --version
    Write-Host "  ✓ Docker installed: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Docker not found. Please install Docker Desktop." -ForegroundColor Red
    Write-Host "    Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check Docker Compose
try {
    $composeVersion = docker-compose --version
    Write-Host "  ✓ Docker Compose installed: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Docker Compose not found." -ForegroundColor Red
    exit 1
}

# Check if Docker is running
try {
    docker ps | Out-Null
    Write-Host "  ✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check .env file
Write-Host "`n[2/6] Checking configuration..." -ForegroundColor Yellow

if (Test-Path ".env") {
    Write-Host "  ✓ .env file found" -ForegroundColor Green
    
    # Check if SMTP is configured
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "your_email@gmail.com" -or $envContent -match "your_app_password") {
        Write-Host "  ⚠ WARNING: .env file contains placeholder values" -ForegroundColor Yellow
        Write-Host "    Please update .env with your actual SMTP credentials" -ForegroundColor Yellow
        Write-Host "    See QUICKSTART.md for instructions" -ForegroundColor Yellow
        
        $continue = Read-Host "`n  Continue anyway? (y/n)"
        if ($continue -ne 'y') {
            Write-Host "`n  Setup cancelled. Please update .env and run again." -ForegroundColor Yellow
            exit 0
        }
    } else {
        Write-Host "  ✓ SMTP configuration appears to be set" -ForegroundColor Green
    }
} else {
    Write-Host "  ✗ .env file not found" -ForegroundColor Red
    exit 1
}

# Check birthdays.csv
Write-Host "`n[3/6] Checking data files..." -ForegroundColor Yellow

if (Test-Path "data/raw/birthdays.csv") {
    $csvContent = Get-Content "data/raw/birthdays.csv"
    $recordCount = ($csvContent | Measure-Object).Count - 1  # Exclude header
    Write-Host "  ✓ birthdays.csv found with $recordCount records" -ForegroundColor Green
    
    # Check if any birthday is today
    $today = Get-Date -Format "MM-dd"
    $todayAlt = Get-Date -Format "yyyy-MM-dd"
    
    $hasTodayBirthday = $false
    foreach ($line in $csvContent) {
        if ($line -match $today -or $line -match $todayAlt) {
            $hasTodayBirthday = $true
            break
        }
    }
    
    if ($hasTodayBirthday) {
        Write-Host "  🎂 Found birthday(s) matching today's date - emails will be sent!" -ForegroundColor Green
    } else {
        $todayDate = Get-Date -Format "yyyy-MM-dd"
        Write-Host "  ℹ No birthdays match today's date ($todayDate)" -ForegroundColor Yellow
        Write-Host "    Add a test record to see email in action:" -ForegroundColor Yellow
        Write-Host "    Test User,your.email@example.com,$todayDate" -ForegroundColor Cyan
    }
} else {
    Write-Host "  ✗ birthdays.csv not found" -ForegroundColor Red
    exit 1
}

# Create logs directory if it doesn't exist
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

# Start Docker services
Write-Host "`n[4/6] Starting Docker services..." -ForegroundColor Yellow
Write-Host "  This may take 2-3 minutes on first run..." -ForegroundColor Gray

try {
    docker-compose up -d
    Write-Host "  ✓ Docker services started" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Failed to start Docker services" -ForegroundColor Red
    Write-Host "  Error: $_" -ForegroundColor Red
    exit 1
}

# Wait for services to be healthy
Write-Host "`n[5/6] Waiting for services to be ready..." -ForegroundColor Yellow
Write-Host "  This may take up to 2 minutes..." -ForegroundColor Gray

$maxWaitTime = 120  # 2 minutes
$waitTime = 0
$checkInterval = 5

while ($waitTime -lt $maxWaitTime) {
    Start-Sleep -Seconds $checkInterval
    $waitTime += $checkInterval
    
    # Check if webserver is responding
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8080/health" -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "  ✓ Airflow webserver is ready!" -ForegroundColor Green
            break
        }
    } catch {
        Write-Host "  ⏳ Still waiting... ($waitTime/$maxWaitTime seconds)" -ForegroundColor Gray
    }
}

if ($waitTime -ge $maxWaitTime) {
    Write-Host "  ⚠ Timeout waiting for services. They may still be starting..." -ForegroundColor Yellow
    Write-Host "    Check status with: docker-compose ps" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ All services are ready!" -ForegroundColor Green
}

# Display service status
Write-Host "`n[6/6] Checking service status..." -ForegroundColor Yellow
docker-compose ps

# Success message
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Open Airflow UI: http://localhost:8080" -ForegroundColor White
Write-Host "   Login: airflow / airflow" -ForegroundColor Gray
Write-Host "`n2. Find 'birthday_email_scheduler' DAG" -ForegroundColor White
Write-Host "   Toggle it ON (switch on the left)" -ForegroundColor Gray
Write-Host "`n3. Click the Play button (▶) to trigger manually" -ForegroundColor White
Write-Host "   Or wait for scheduled run at 9:00 AM daily" -ForegroundColor Gray

Write-Host "`n📚 Documentation:" -ForegroundColor Cyan
Write-Host "   • Quick Start: QUICKSTART.md" -ForegroundColor White
Write-Host "   • Full Guide: README.md" -ForegroundColor White

Write-Host "`n🛑 To stop the system:" -ForegroundColor Cyan
Write-Host "   docker-compose down" -ForegroundColor White

Write-Host "`n🔍 View logs:" -ForegroundColor Cyan
Write-Host "   docker-compose logs -f airflow-webserver" -ForegroundColor White
Write-Host "   docker-compose logs -f airflow-scheduler" -ForegroundColor White

Write-Host "`n========================================" -ForegroundColor Cyan

# Open browser
$openBrowser = Read-Host "`nOpen Airflow UI in browser now? (y/n)"
if ($openBrowser -eq 'y') {
    Start-Process "http://localhost:8080"
    Write-Host "✓ Opening browser..." -ForegroundColor Green
}

Write-Host "`nSetup complete! 🎉" -ForegroundColor Green
