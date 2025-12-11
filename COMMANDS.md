# 🎂 Birthday Email Scheduler - Command Reference

## 🚀 Setup & Start

```powershell
# First-time setup (automatic)
.\setup.ps1

# Manual setup (if needed)
docker-compose up -d
```

## 🛑 Stop & Shutdown

```powershell
# Stop services (data preserved)
docker-compose stop

# Stop and remove containers (data preserved)
docker-compose down

# Remove everything including data (CAUTION!)
docker-compose down -v

# Or use the helper script
.\stop.ps1
```

## 🔄 Restart & Reload

```powershell
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart airflow-scheduler
docker-compose restart airflow-webserver

# Restart after code changes
docker-compose restart airflow-scheduler airflow-webserver
```

## 📊 Status & Monitoring

```powershell
# View service status
docker-compose ps

# View logs (follow mode)
docker-compose logs -f airflow-webserver
docker-compose logs -f airflow-scheduler

# View logs (last 100 lines)
docker-compose logs --tail=100 airflow-webserver

# Check container resource usage
docker stats
```

## 🐳 Docker Commands

```powershell
# List all containers
docker ps -a

# List all volumes
docker volume ls

# Remove unused resources
docker system prune

# Remove unused volumes
docker volume prune

# View Docker disk usage
docker system df
```

## ✈️ Airflow Commands

```powershell
# List all DAGs
docker-compose exec airflow-webserver airflow dags list

# Trigger DAG manually
docker-compose exec airflow-webserver airflow dags trigger birthday_email_scheduler

# Test specific task
docker-compose exec airflow-webserver airflow tasks test birthday_email_scheduler extract_data 2024-12-11

# List users
docker-compose exec airflow-webserver airflow users list

# Create new user
docker-compose exec airflow-webserver airflow users create `
    --username admin `
    --firstname Admin `
    --lastname User `
    --role Admin `
    --email admin@example.com `
    --password admin

# Reset Airflow database (CAUTION!)
docker-compose exec airflow-webserver airflow db reset
```

## 📝 File Operations

```powershell
# Edit birthday data
notepad data\raw\birthdays.csv

# Edit email configuration
notepad .env

# View cleaned data
Get-Content data\processed\cleaned_birthdays.csv

# View logs
Get-Content logs\dag_id=birthday_email_scheduler\*.log

# Test pipeline locally
python test_pipeline.py
```

## 🔍 Debugging

```powershell
# Check if port 8080 is in use
netstat -ano | findstr "8080"

# Check if port 5432 is in use (PostgreSQL)
netstat -ano | findstr "5432"

# Access PostgreSQL database
docker-compose exec postgres psql -U airflow -d airflow

# Access container shell
docker-compose exec airflow-webserver bash

# View environment variables
docker-compose exec airflow-webserver env

# Check Python packages in container
docker-compose exec airflow-webserver pip list
```

## 📧 Email Testing

```powershell
# Test SMTP connection (in Python)
docker-compose exec airflow-webserver python -c "
import smtplib
import os
smtp_host = os.getenv('AIRFLOW__SMTP__SMTP_HOST', 'smtp.gmail.com')
smtp_port = int(os.getenv('AIRFLOW__SMTP__SMTP_PORT', 587))
smtp_user = os.getenv('AIRFLOW__SMTP__SMTP_USER', '')
smtp_password = os.getenv('AIRFLOW__SMTP__SMTP_PASSWORD', '')
try:
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        print('✓ SMTP connection successful')
except Exception as e:
    print(f'✗ SMTP connection failed: {e}')
"
```

## 🧪 Testing

```powershell
# Test pipeline components
python test_pipeline.py

# Test DAG syntax
docker-compose exec airflow-webserver python /opt/airflow/dags/birthday_email_dag.py

# List Airflow tasks
docker-compose exec airflow-webserver airflow tasks list birthday_email_scheduler

# Test extract task
docker-compose exec airflow-webserver airflow tasks test birthday_email_scheduler extract_data 2024-12-11

# Test transform task
docker-compose exec airflow-webserver airflow tasks test birthday_email_scheduler transform_data 2024-12-11

# Test check birthdays task
docker-compose exec airflow-webserver airflow tasks test birthday_email_scheduler check_birthdays 2024-12-11
```

## 🔧 Configuration

```powershell
# Edit Docker Compose configuration
notepad docker-compose.yaml

# Edit Airflow DAG
notepad dags\birthday_email_dag.py

# Edit email template
notepad scripts\email_utils.py

# Edit data transformation rules
notepad scripts\transform.py

# Edit application config
notepad config\config.yaml
```

## 🗄️ Database Operations

```powershell
# Connect to PostgreSQL
docker-compose exec postgres psql -U airflow -d airflow

# SQL commands (inside psql):
# \dt                    - List tables
# \d table_name          - Describe table
# SELECT * FROM dag;     - View DAGs
# SELECT * FROM dag_run; - View DAG runs
# \q                     - Quit
```

## 🔐 Security

```powershell
# Generate new Fernet key (for Airflow encryption)
docker-compose exec airflow-webserver python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Update Fernet key in docker-compose.yaml:
# AIRFLOW__CORE__FERNET_KEY: 'your_new_key_here'
```

## 📦 Backup & Restore

```powershell
# Backup birthday data
Copy-Item data\raw\birthdays.csv data\raw\birthdays.csv.backup

# Backup PostgreSQL database
docker-compose exec postgres pg_dump -U airflow airflow > backup.sql

# Restore PostgreSQL database
Get-Content backup.sql | docker-compose exec -T postgres psql -U airflow airflow

# Backup logs
Compress-Archive -Path logs -DestinationPath logs_backup_$(Get-Date -Format 'yyyyMMdd').zip
```

## 🔄 Updates

```powershell
# Update Docker images
docker-compose pull

# Rebuild containers
docker-compose up -d --build

# Update Python packages (in container)
docker-compose exec airflow-webserver pip install --upgrade -r /opt/airflow/requirements.txt

# Restart after updates
docker-compose restart
```

## 📈 Performance

```powershell
# View resource usage
docker stats

# View container processes
docker-compose top

# Check Airflow task instances
docker-compose exec airflow-webserver airflow tasks states-for-dag-run birthday_email_scheduler <dag_run_id>

# Clean old logs (keeps last 30 days)
docker-compose exec airflow-webserver airflow db clean --clean-before-timestamp "$(Get-Date (Get-Date).AddDays(-30) -Format 'yyyy-MM-dd')"
```

## 🌐 Network

```powershell
# List Docker networks
docker network ls

# Inspect network
docker network inspect birthday_sch_default

# Test connectivity between containers
docker-compose exec airflow-webserver ping postgres
```

## 🎯 Quick Workflows

### Add New Birthday & Test
```powershell
# 1. Add birthday with today's date
Add-Content data\raw\birthdays.csv "`nTest User,test@example.com,$(Get-Date -Format 'yyyy-MM-dd')"

# 2. Trigger DAG
# Go to http://localhost:8080 and click Play button

# 3. Check email inbox
```

### Update Email Template & Reload
```powershell
# 1. Edit template
notepad scripts\email_utils.py

# 2. Restart scheduler
docker-compose restart airflow-scheduler

# 3. Trigger DAG to test
```

### Check Why Email Didn't Send
```powershell
# 1. Check if birthday was detected
docker-compose logs airflow-scheduler | Select-String "birthday"

# 2. View send_emails task logs in UI
# http://localhost:8080 → DAG → send_emails task → Logs

# 3. Verify SMTP config
docker-compose exec airflow-webserver env | Select-String "SMTP"
```

### Reset Everything
```powershell
# 1. Stop and remove everything
docker-compose down -v

# 2. Clean Docker system
docker system prune -f

# 3. Restart setup
.\setup.ps1
```

## 📱 URLs

- **Airflow UI**: http://localhost:8080
- **PostgreSQL**: localhost:5432
- **Login**: airflow / airflow

## 🆘 Emergency Commands

```powershell
# Kill all Docker containers
docker kill $(docker ps -q)

# Remove all Docker containers
docker rm $(docker ps -a -q)

# Remove all Docker volumes
docker volume rm $(docker volume ls -q)

# Nuclear option - remove everything
docker system prune -a --volumes -f

# Force restart Docker Desktop
Stop-Process -Name "Docker Desktop" -Force
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

## 💡 Aliases (Optional)

Add to PowerShell profile (`notepad $PROFILE`):

```powershell
function airflow-start { docker-compose up -d }
function airflow-stop { docker-compose down }
function airflow-logs { docker-compose logs -f airflow-webserver }
function airflow-restart { docker-compose restart airflow-scheduler airflow-webserver }
function airflow-status { docker-compose ps }
```

---

## 📚 Quick Help

- **Setup Issues**: See `GETTING_STARTED.md`
- **Usage Help**: See `README.md`
- **Architecture**: See `PROJECT_SUMMARY.md`
- **Quick Start**: See `QUICKSTART.md`

---

**Remember**: Most changes to DAGs or scripts require restarting the scheduler:
```powershell
docker-compose restart airflow-scheduler
```
