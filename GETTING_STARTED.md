# GETTING STARTED - Birthday Email Scheduler

Welcome! This is your complete Birthday Email Scheduler built with Apache Airflow, Python, and Docker.

## ⚡ Quick Start (5 Minutes)

### Step 1: Update Email Configuration
```powershell
# Open .env file and update these lines:
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
SMTP_MAIL_FROM=your_email@gmail.com
```

**Get Gmail App Password:**
1. Go to: https://myaccount.google.com/apppasswords
2. Enable 2FA if not already enabled
3. Create password for "Mail"
4. Copy the 16-character password

### Step 2: Add Birthday Data
```powershell
# Edit data/raw/birthdays.csv
# Add real data or test with today's date:
```
```csv
name,email,dob
Your Name,your.email@example.com,2024-12-11
```
Replace `2024-12-11` with **today's date** for immediate testing.

### Step 3: Run Setup
```powershell
# In project directory, run:
.\setup.ps1
```

This will:
- Check prerequisites (Docker, Docker Compose)
- Validate configuration
- Start all Docker services
- Initialize Airflow database
- Create admin user

### Step 4: Access Airflow
1. Open: http://localhost:8080
2. Login: `airflow` / `airflow`
3. Find `birthday_email_scheduler` DAG
4. Toggle it **ON**
5. Click **Play button (▶)** to trigger

### Step 5: Check Results
- Monitor execution in Graph view
- Click tasks to view logs
- Check your email for birthday message!

## 📁 Project Structure

```
Birthday_sch/
├── 📄 docker-compose.yaml       # Docker orchestration
├── 📄 .env                      # SMTP credentials (UPDATE THIS!)
├── 📄 requirements.txt          # Python dependencies
│
├── 📂 dags/
│   └── birthday_email_dag.py    # Main workflow definition
│
├── 📂 scripts/
│   ├── extract.py               # Read data from CSV
│   ├── transform.py             # Clean and validate data
│   ├── load.py                  # Save processed data
│   └── email_utils.py           # Send birthday emails
│
├── 📂 data/
│   ├── raw/
│   │   └── birthdays.csv        # INPUT: Add birthdays here
│   └── processed/
│       └── cleaned_birthdays.csv # OUTPUT: Cleaned data
│
├── 📂 config/
│   └── config.yaml              # Configuration settings
│
├── 📄 README.md                 # Full documentation
├── 📄 QUICKSTART.md             # Quick setup guide
├── 📄 PROJECT_SUMMARY.md        # Technical overview
├── 📄 setup.ps1                 # Automated setup
└── 📄 stop.ps1                  # Stop services
```

## 🔄 How It Works

**Daily at 9:00 AM**, the system:

1. **EXTRACT** → Reads `birthdays.csv`
2. **TRANSFORM** → Cleans data, validates emails, parses dates
3. **CHECK** → Finds birthdays matching today's date
4. **SEND** → Sends personalized HTML emails
5. **LOG** → Generates summary report

## 📊 What Each File Does

### Core Workflow
- **`birthday_email_dag.py`**: Orchestrates the entire process
- **`extract.py`**: Reads birthday data from CSV/Excel files
- **`transform.py`**: Cleans data (removes duplicates, validates emails)
- **`load.py`**: Saves cleaned data to processed folder
- **`email_utils.py`**: Sends beautiful HTML birthday emails

### Configuration
- **`.env`**: SMTP email settings (**UPDATE THIS FIRST!**)
- **`config.yaml`**: Application settings (schedule, rules, etc.)
- **`docker-compose.yaml`**: Docker services configuration

### Data
- **`data/raw/birthdays.csv`**: Your input data (names, emails, birthdays)
- **`data/processed/`**: Cleaned output data

### Helpers
- **`setup.ps1`**: Automated setup script
- **`stop.ps1`**: Stop services script
- **`test_pipeline.py`**: Test individual components

## 🎯 Common Tasks

### Add New Birthday
```powershell
# Edit data/raw/birthdays.csv and add:
New Person,new.email@example.com,1990-05-15
```

### Test Immediately
```powershell
# Add a birthday with TODAY's date to birthdays.csv
Test User,your.email@example.com,2024-12-11

# Trigger DAG manually in Airflow UI
```

### View Logs
```powershell
# Airflow UI: Click task → Logs button
# Or in terminal:
docker-compose logs -f airflow-scheduler
docker-compose logs -f airflow-webserver
```

### Change Schedule
```python
# Edit dags/birthday_email_dag.py
schedule_interval='0 9 * * *',  # Daily at 9 AM
```

Common schedules:
- `'0 9 * * *'` - Daily at 9 AM
- `'0 */6 * * *'` - Every 6 hours
- `'0 9 * * 1'` - Every Monday at 9 AM

### Stop System
```powershell
.\stop.ps1
# Or manually:
docker-compose down
```

### Restart System
```powershell
docker-compose up -d
```

## 🐛 Troubleshooting

### DAG Not Showing?
```powershell
docker-compose restart airflow-scheduler
# Wait 30 seconds and refresh browser
```

### Email Not Sending?
1. Verify `.env` has correct App Password
2. Check Gmail has 2FA enabled
3. View task logs: Click `send_emails` task → Logs

### No Birthdays Found?
1. Check date format in CSV: `YYYY-MM-DD`
2. Verify dates match today: Check `check_birthdays` task logs
3. Add test record with today's date

### Docker Issues?
```powershell
# Check Docker is running
docker ps

# Restart Docker Desktop

# Check logs
docker-compose logs
```

## 📚 Documentation Files

- **`README.md`** - Complete documentation with detailed setup
- **`QUICKSTART.md`** - 5-minute quick start guide
- **`PROJECT_SUMMARY.md`** - Technical architecture and design
- **`THIS FILE`** - Getting started overview

## 🔐 Security Notes

1. **Never commit `.env`** to Git - it's in `.gitignore`
2. Use **App Password** for Gmail (not your account password)
3. Change default Airflow password in production
4. Keep `birthdays.csv` private (contains personal data)

## 💡 Pro Tips

1. **Test First**: Add today's date to CSV before going live
2. **Check Logs**: Always review logs after first run
3. **Backup Data**: Keep backup of birthdays.csv
4. **Monitor Daily**: Check Airflow UI daily for errors
5. **Update Regularly**: Keep dependencies up to date

## 🎓 Learning More

**Apache Airflow:**
- Official Docs: https://airflow.apache.org/docs/
- Concepts: https://airflow.apache.org/docs/apache-airflow/stable/concepts/

**Docker:**
- Docker Docs: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/

**Python Pandas:**
- Pandas Docs: https://pandas.pydata.org/docs/

## ✅ Checklist for Success

- [ ] Docker Desktop installed and running
- [ ] `.env` updated with Gmail credentials
- [ ] Gmail 2FA enabled and App Password created
- [ ] `birthdays.csv` has test data with today's date
- [ ] Ran `.\setup.ps1` successfully
- [ ] Accessed Airflow UI at http://localhost:8080
- [ ] DAG toggled ON
- [ ] Manually triggered DAG
- [ ] Checked task logs for errors
- [ ] Received test birthday email

## 🚀 Next Steps After Setup

1. **Verify Test Email**: Check inbox for birthday message
2. **Add Real Data**: Update `birthdays.csv` with actual birthdays
3. **Customize Template**: Edit email HTML in `email_utils.py`
4. **Set Schedule**: Adjust run time if needed (default: 9 AM)
5. **Monitor Daily**: Check Airflow UI for successful runs

## 🆘 Need Help?

1. **Check Logs First**: Most issues are visible in logs
2. **Review Troubleshooting**: See README.md troubleshooting section
3. **Test Components**: Run `python test_pipeline.py`
4. **Verify Config**: Double-check `.env` file
5. **Check Services**: Run `docker-compose ps`

## 🎉 Success Indicators

You'll know it's working when:
- ✅ All Docker services show "healthy" status
- ✅ Airflow UI loads successfully
- ✅ DAG runs without errors (all tasks green)
- ✅ Birthday email arrives in inbox
- ✅ Summary task shows correct statistics

---

## Ready to Start?

```powershell
# 1. Update .env with your email credentials
# 2. Add test birthday with today's date
# 3. Run setup:
.\setup.ps1

# 4. Open browser to http://localhost:8080
# 5. Login: airflow / airflow
# 6. Enable and trigger the DAG
# 7. Check your email! 🎂
```

**That's it! You're ready to automate birthday emails! 🚀**

---

*Need more details? See README.md for complete documentation.*
*Having issues? Check troubleshooting section in README.md.*
*Want to customize? See PROJECT_SUMMARY.md for architecture details.*
