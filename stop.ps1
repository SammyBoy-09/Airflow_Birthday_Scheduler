# Birthday Email Scheduler - Stop Script
# Run this script to stop all services

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BIRTHDAY EMAIL SCHEDULER - STOP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nWhat would you like to do?" -ForegroundColor Yellow
Write-Host "1. Stop services (data will be preserved)" -ForegroundColor White
Write-Host "2. Stop and remove containers (data will be preserved)" -ForegroundColor White
Write-Host "3. Stop and remove everything including data (CAUTION)" -ForegroundColor Red
Write-Host "4. Cancel" -ForegroundColor Gray

$choice = Read-Host "`nEnter choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host "`nStopping services..." -ForegroundColor Yellow
        docker-compose stop
        Write-Host "✓ Services stopped. Data preserved." -ForegroundColor Green
        Write-Host "To start again: docker-compose start" -ForegroundColor Gray
    }
    "2" {
        Write-Host "`nStopping and removing containers..." -ForegroundColor Yellow
        docker-compose down
        Write-Host "✓ Containers removed. Data preserved in volumes." -ForegroundColor Green
        Write-Host "To start again: docker-compose up -d" -ForegroundColor Gray
    }
    "3" {
        $confirm = Read-Host "`nAre you sure? This will delete all data! (yes/no)"
        if ($confirm -eq "yes") {
            Write-Host "`nRemoving everything..." -ForegroundColor Red
            docker-compose down -v
            Write-Host "✓ Everything removed including data." -ForegroundColor Green
            Write-Host "To start again: docker-compose up -d" -ForegroundColor Gray
        } else {
            Write-Host "`nCancelled." -ForegroundColor Yellow
        }
    }
    "4" {
        Write-Host "`nCancelled." -ForegroundColor Yellow
    }
    default {
        Write-Host "`nInvalid choice. Cancelled." -ForegroundColor Red
    }
}

Write-Host ""
