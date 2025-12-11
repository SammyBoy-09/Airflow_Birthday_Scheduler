# 🎂 Birthday Email Scheduler - Complete Setup Guide

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/SammyBoy-09/Airflow_Birthday_Scheduler)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.8.0-red)](https://airflow.apache.org/)
[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Required-blue)](https://www.docker.com/)

## 📖 Overview

Automated birthday email system built with Apache Airflow that:
- ✅ Extracts birthday data from CSV files
- ✅ Cleans and validates data (emails, dates, duplicates)
- ✅ Checks for today's birthdays
- ✅ Sends personalized HTML emails automatically
- ✅ Runs daily at 9:00 AM IST
- ✅ Logs detailed execution summaries

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites

Before starting, ensure you have:
- ✅ **Docker Desktop** installed and running
- ✅ **Git** (to clone the repository)
- ✅ **Gmail account** with 2FA enabled
- ✅ **4GB+ RAM** available for Docker

### Step 1: Clone the Repository

```powershell
# Clone the repository
git clone https://github.com/SammyBoy-09/Airflow_Birthday_Scheduler.git

# Navigate to project directory
cd Airflow_Birthday_Scheduler
```

### Step 2: Configure Email Settings

1. **Get Gmail App Password:**
   - Visit: https://myaccount.google.com/apppasswords
   - Enable 2-Factor Authentication if not already enabled
   - Create password for "Mail"
   - Copy the 16-character password

2. **Update `.env` file:**
   ```env
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_16_char_app_password
   SMTP_MAIL_FROM=your_email@gmail.com
   ```

   ⚠️ **Important**: Never commit the `.env` file to Git!

### Step 3: Add Birthday Data

Edit `data/raw/birthdays.csv` and add birthday records:

```csv
name,email,dob
John Doe,john.doe@example.com,1990-01-15
Jane Smith,jane.smith@example.com,1985-05-20
```

**For immediate testing**, add a record with **today's date**:
```csv
Test User,your.email@example.com,2025-12-11
```

### Step 4: Start Docker Services

```powershell
# Make sure Docker Desktop is running

# Start all services
docker-compose up -d

# Wait 2-3 minutes for initialization
# Check status
docker-compose ps
```

Expected output:
```
NAME                               STATUS
birthday_sch-airflow-scheduler-1   Up (healthy)
birthday_sch-airflow-webserver-1   Up (healthy)
birthday_sch-postgres-1            Up (healthy)
```

### Step 5: Access Airflow UI

1. Open browser: **http://localhost:8080**
2. Login credentials:
   - Username: `airflow`
   - Password: `airflow`

### Step 6: Enable and Run DAG

1. Find `birthday_email_scheduler` in the DAG list
2. Toggle the switch to **ON** (left side)
3. Click the **▶ Play button** (right side)
4. Select **"Trigger DAG"**
5. Monitor execution in **Graph** view

### Step 7: Verify Success

- ✅ All tasks turn **green** (success)
- ✅ Check the **log_summary** task for detailed report
- ✅ Check your **email inbox** for birthday message(s)

---

## 📁 Project Structure

```
Airflow_Birthday_Scheduler/
├── 📂 dags/
│   └── birthday_email_dag.py       # Main Airflow DAG
│
├── 📂 scripts/
│   ├── extract.py                  # Data extraction
│   ├── transform.py                # Data cleaning & validation
│   ├── load.py                     # Data saving
│   └── email_utils.py              # Email sending
│
├── 📂 data/      
│   ├── raw/birthdays.csv           # INPUT: Your birthday data
│   └── processed/                  # OUTPUT: Cleaned data
│
├── 📂 config/
│   └── config.yaml                 # Configuration settings
│
├── docker-compose.yaml             # Docker orchestration
├── .env                            # Email credentials (CREATE THIS!)
├── requirements.txt                # Python dependencies
│
├── README.md                       # Project overview
├── QUICKSTART.md                   # 5-minute quick start
├── GETTING_STARTED.md              # Detailed beginner guide
├── PROJECT_SUMMARY.md              # Technical documentation
├── COMMANDS.md                     # Command reference
└── INDEX.md                        # Project navigation
```

---

## 🔧 Configuration

### Email Settings (.env)

```env
# Gmail SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
SMTP_MAIL_FROM=your_email@gmail.com
```

### Schedule (IST Timezone)

Default: Daily at 9:00 AM IST

To change, edit `dags/birthday_email_dag.py`:
```python
schedule_interval='0 9 * * *',  # Cron expression
```

**Common schedules:**
- `'0 9 * * *'` - Daily at 9 AM
- `'0 */6 * * *'` - Every 6 hours
- `'0 9 * * 1'` - Every Monday at 9 AM

### Data Format

`data/raw/birthdays.csv` format:
```csv
name,email,dob
John Doe,john.doe@example.com,1990-01-15
```

**Supported date formats:**
- `YYYY-MM-DD` (recommended)
- `DD/MM/YYYY`
- `MM/DD/YYYY`

---

## 🔄 How It Works

```
┌─────────────────────────────────────────────────────┐
│  DAILY AT 9:00 AM IST                               │
└─────────────────────────────────────────────────────┘
                    ↓
         ┌──────────────────────┐
         │  1. EXTRACT DATA     │
         │  Read birthdays.csv  │
         └──────────────────────┘
                    ↓
         ┌──────────────────────┐
         │  2. TRANSFORM DATA   │
         │  - Validate emails   │
         │  - Parse dates       │
         │  - Remove duplicates │
         └──────────────────────┘
                    ↓
         ┌──────────────────────┐
         │  3. CHECK BIRTHDAYS  │
         │  Find today's matches│
         └──────────────────────┘
                    ↓
         ┌──────────────────────┐
         │  4. SEND EMAILS      │
         │  HTML birthday msgs  │
         └──────────────────────┘
                    ↓
         ┌──────────────────────┐
         │  5. LOG SUMMARY      │
         │  Report with details │
         └──────────────────────┘
```

---

## 📊 Monitoring & Logs

### View DAG Execution

1. Go to Airflow UI: http://localhost:8080
2. Click on `birthday_email_scheduler`
3. View **Graph** or **Grid** for task status
4. Click any task → **Logs** to view details

### Summary Report Example

```
========================================
BIRTHDAY EMAIL SCHEDULER - DAILY REPORT
========================================
Run Date: 2025-12-11 09:00:00

EXTRACTION:
- Records extracted: 15

TRANSFORMATION:
- Records after cleaning: 15
- Records removed: 0

BIRTHDAY CHECK:
- Birthdays today: 2

BIRTHDAY RECIPIENTS:
1. Kevin Hart (kevin.hart@example.com)
2. John Doe (john.doe@example.com)

EMAIL SENDING:
- Emails sent successfully: 2
- Emails failed: 0

========================================
```

### Command Line Logs

```powershell
# View webserver logs
docker-compose logs -f airflow-webserver

# View scheduler logs
docker-compose logs -f airflow-scheduler

# View all logs
docker-compose logs -f
```

---

## 🛑 Stopping the System

```powershell
# Stop services (data preserved)
docker-compose stop

# Stop and remove containers (data preserved)
docker-compose down

# Remove everything including data
docker-compose down -v
```

---

## 🐛 Troubleshooting

### Issue: Docker not starting

**Solution:**
```powershell
# Check if Docker Desktop is running
docker version

# Start Docker Desktop
# Then run:
docker-compose up -d
```

### Issue: DAG not appearing

**Solution:**
```powershell
# Restart scheduler
docker-compose restart airflow-scheduler

# Wait 30 seconds and refresh browser
```

### Issue: Email not sending

**Check:**
1. ✅ `.env` file has correct App Password
2. ✅ Gmail 2FA is enabled
3. ✅ App Password is 16 characters (no spaces)
4. ✅ Check task logs in Airflow UI

**Test SMTP connection:**
```powershell
docker-compose exec airflow-webserver python -c "
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your_email@gmail.com', 'your_app_password')
print('✓ SMTP connection successful')
server.quit()
"
```

### Issue: No birthdays found

**Check:**
1. Verify date format in CSV: `YYYY-MM-DD`
2. Ensure date matches today's date
3. Check `check_birthdays` task logs

### Issue: Port 8080 already in use

**Solution:**
```powershell
# Find process using port 8080
netstat -ano | findstr "8080"

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Or change port in docker-compose.yaml
# "8081:8080" instead of "8080:8080"
```

---

## 🔐 Security Best Practices

1. ✅ **Never commit `.env`** - It's in `.gitignore`
2. ✅ Use **App Passwords**, not account password
3. ✅ Change **Airflow credentials** in production
4. ✅ Restrict **Airflow UI access** (firewall/VPN)
5. ✅ Keep **dependencies updated**

---

## 📦 Dependencies

### Docker Services
- PostgreSQL 13
- Apache Airflow 2.8.0
- Python 3.10

### Python Packages
- pandas 2.0+
- pendulum 2.1+
- psycopg2-binary
- pydantic 2.0+
- openpyxl

See `requirements.txt` for complete list.

---

## 🎨 Customization

### Change Email Template

Edit `scripts/email_utils.py` → `create_birthday_email()` method

### Add Data Validation Rules

Edit `scripts/transform.py` → `BirthdayDataCleaner` class

### Modify Schedule

Edit `dags/birthday_email_dag.py` → `schedule_interval`

### Add New Data Sources

Extend `scripts/extract.py` to support databases, APIs, etc.

---

## 📚 Documentation

- **README.md** - Project overview
- **QUICKSTART.md** - 5-minute setup
- **GETTING_STARTED.md** - Detailed guide
- **PROJECT_SUMMARY.md** - Architecture
- **COMMANDS.md** - All commands
- **INDEX.md** - Navigation

---

## 📄 License

MIT License - See LICENSE file for details

---

## ✅ Setup Checklist

Before running:
- [ ] Docker Desktop installed and running
- [ ] Repository cloned
- [ ] `.env` file created with Gmail credentials
- [ ] Gmail 2FA enabled and App Password generated
- [ ] `birthdays.csv` populated with test data
- [ ] Docker services started (`docker-compose up -d`)
- [ ] Airflow UI accessible (http://localhost:8080)
- [ ] DAG enabled and triggered
- [ ] Test email received

---

## 🎉 Success!

If you've completed all steps and received a test email, congratulations! 🎂

The system is now ready to:
- Run automatically every day at 9 AM IST
- Send birthday emails to matching recipients
- Log detailed execution summaries

**Next steps:**
1. Add real birthday data to `birthdays.csv`
2. Customize email template if desired
3. Monitor daily runs via Airflow UI
4. Check logs for any issues

---

**Repository:** https://github.com/SammyBoy-09/Airflow_Birthday_Scheduler
