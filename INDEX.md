# 🎂 Birthday Email Scheduler - Complete Project Index

## 📋 Project Overview

An automated birthday email system built with Apache Airflow, Python, and Docker that:
- ✅ Extracts birthday data from CSV files
- ✅ Transforms and cleans the data
- ✅ Checks for today's birthdays
- ✅ Sends personalized HTML emails automatically
- ✅ Runs daily at 9:00 AM (configurable)

**Status**: ✅ Production Ready
**Version**: 1.0.0
**Last Updated**: December 2024

---

## 🗂️ File Structure & Purpose

### 📂 Root Directory
```
Birthday_sch/
│
├── 📄 docker-compose.yaml        ⭐ Docker orchestration (PostgreSQL, Airflow)
├── 📄 .env                       🔐 SMTP email credentials (UPDATE FIRST!)
├── 📄 requirements.txt           📦 Python dependencies
├── 📄 .gitignore                 🚫 Git ignore rules
│
├── 📄 README.md                  📚 Complete documentation (20+ pages)
├── 📄 GETTING_STARTED.md         🚀 New user guide (start here!)
├── 📄 QUICKSTART.md              ⚡ 5-minute setup guide
├── 📄 PROJECT_SUMMARY.md         🏗️ Technical architecture & design
├── 📄 COMMANDS.md                💻 Command reference (all commands)
├── 📄 INDEX.md                   📑 This file
│
├── 📄 setup.ps1                  🔧 Automated setup script (Windows)
├── 📄 stop.ps1                   🛑 Service stop script (Windows)
└── 📄 test_pipeline.py           🧪 Component testing script
```

### 📂 dags/ - Airflow DAG Definitions
```
dags/
└── 📄 birthday_email_dag.py      ⭐ Main workflow orchestration
                                     - Defines 5 tasks (Extract→Transform→Check→Send→Log)
                                     - Schedule: Daily at 9 AM
                                     - Uses XCom for data passing
```

### 📂 scripts/ - Python ETL Modules
```
scripts/
├── 📄 __init__.py                📦 Package initialization
├── 📄 extract.py                 📥 Extract: Read CSV/Excel files
├── 📄 transform.py               🔄 Transform: Clean & validate data
├── 📄 load.py                    💾 Load: Save processed data
└── 📄 email_utils.py             📧 Email: Send birthday emails via SMTP
```

**Key Functions:**
- `extract()` - Read birthday data from files
- `transform()` - Clean, validate, parse dates
- `load()` - Save to CSV/Excel
- `EmailSender` - Send HTML emails
- `send_birthday_emails_task()` - Airflow task wrapper

### 📂 data/ - Data Storage
```
data/
├── raw/
│   └── 📄 birthdays.csv          📥 INPUT: Names, emails, DOBs (EDIT THIS!)
└── processed/
    ├── 📄 .gitkeep               
    └── 📄 cleaned_birthdays.csv  📤 OUTPUT: Cleaned data
```

**Data Format (birthdays.csv):**
```csv
name,email,dob
John Doe,john.doe@example.com,1990-01-15
Jane Smith,jane.smith@example.com,1985-05-20
```

### 📂 config/ - Configuration Files
```
config/
└── 📄 config.yaml                ⚙️ Application settings
                                     - Schedule configuration
                                     - Cleaning rules
                                     - Email settings
```

### 📂 logs/ - Airflow Logs
```
logs/                             📊 Airflow execution logs
└── (generated automatically)
```

### 📂 plugins/ - Custom Airflow Plugins
```
plugins/                          🔌 Extensibility (currently empty)
└── 📄 .gitkeep
```

---

## 🎯 Quick Navigation by Task

### 🆕 First Time Setup
1. Read: `GETTING_STARTED.md`
2. Follow: `QUICKSTART.md`
3. Run: `setup.ps1`

### 📖 Learning & Understanding
- **How it works**: `PROJECT_SUMMARY.md` → Workflow Diagram section
- **Full documentation**: `README.md`
- **Architecture**: `PROJECT_SUMMARY.md` → Component Details

### 💻 Daily Operations
- **Commands**: `COMMANDS.md`
- **View logs**: Airflow UI → Tasks → Logs
- **Add birthdays**: Edit `data/raw/birthdays.csv`

### 🔧 Configuration & Customization
- **Email settings**: Edit `.env`
- **Email template**: Edit `scripts/email_utils.py` → `create_birthday_email()`
- **Schedule**: Edit `dags/birthday_email_dag.py` → `schedule_interval`
- **Cleaning rules**: Edit `scripts/transform.py` → `BirthdayDataCleaner`

### 🐛 Troubleshooting
- **Common issues**: `README.md` → Troubleshooting section
- **Test components**: Run `python test_pipeline.py`
- **Check services**: `docker-compose ps`
- **View logs**: `docker-compose logs -f airflow-scheduler`

### 🚀 Advanced Topics
- **Architecture**: `PROJECT_SUMMARY.md` → Architecture section
- **Scaling**: `PROJECT_SUMMARY.md` → Scaling Considerations
- **Security**: `PROJECT_SUMMARY.md` → Security Considerations
- **Future enhancements**: `PROJECT_SUMMARY.md` → Future Enhancements

---

## 📊 Data Flow Visualization

```
USER INPUT                    AIRFLOW DAG                     OUTPUT
──────────                    ───────────                     ──────

birthdays.csv  ──┐
                 │
                 ├──→ [EXTRACT]  ──→  DataFrame (in memory)
                 │      ↓
                 │      • Read CSV
                 │      • Validate file
                 │
                 ├──→ [TRANSFORM] ──→  Cleaned DataFrame
                 │      ↓
                 │      • Trim whitespace
                 │      • Validate emails
                 │      • Parse dates
                 │      • Remove duplicates
                 │
                 ├──→ [LOAD]      ──→  cleaned_birthdays.csv
                 │      ↓
                 │      • Save to processed/
                 │
                 ├──→ [CHECK]     ──→  Birthday List
                 │      ↓
                 │      • Filter by date
                 │      • Match month & day
                 │
                 ├──→ [SEND]      ──→  📧 Birthday Emails
                 │      ↓
                 │      • Create HTML email
                 │      • Send via SMTP
                 │      • Track results
                 │
                 └──→ [LOG]       ──→  📊 Summary Report
                        ↓
                        • Statistics
                        • Success/Failure counts
```

---

## 🔗 Dependencies & Integrations

### Docker Services
- **PostgreSQL** (port 5432): Airflow metadata database
- **Airflow Webserver** (port 8080): Web UI
- **Airflow Scheduler**: Task execution engine
- **Airflow Init**: Database initialization

### Python Libraries
- `apache-airflow==2.8.0` - Workflow orchestration
- `pandas>=2.0.0` - Data manipulation
- `openpyxl>=3.1.0` - Excel support
- `python-dotenv>=1.0.0` - Environment variables
- `psycopg2-binary>=2.9.0` - PostgreSQL driver
- `pydantic>=2.0.0` - Data validation

### External Services
- **Gmail SMTP** (smtp.gmail.com:587): Email delivery
- **Docker Hub**: Container images

---

## 📝 Configuration Files Explained

### `.env` - Environment Variables
```env
SMTP_HOST=smtp.gmail.com          # Email server
SMTP_PORT=587                     # TLS port
SMTP_USER=your_email@gmail.com    # Gmail address
SMTP_PASSWORD=app_password_here   # 16-char App Password
SMTP_MAIL_FROM=your_email@gmail.com
```
⚠️ **Critical**: Update this before first use!

### `docker-compose.yaml` - Docker Configuration
- Defines 4 services (postgres, webserver, scheduler, init)
- Mounts local directories into containers
- Sets environment variables
- Configures health checks

### `config/config.yaml` - Application Settings
- Data source/destination paths
- Email configuration
- Cleaning rules
- Schedule settings
- Logging configuration

---

## 🎓 Learning Path

### Beginner (Day 1)
1. ✅ Read `GETTING_STARTED.md`
2. ✅ Follow `QUICKSTART.md`
3. ✅ Run `setup.ps1`
4. ✅ Test with today's date
5. ✅ Verify email received

### Intermediate (Week 1)
1. ✅ Understand `PROJECT_SUMMARY.md` → Workflow section
2. ✅ Explore Airflow UI
3. ✅ Review task logs
4. ✅ Customize email template
5. ✅ Add real birthday data

### Advanced (Month 1)
1. ✅ Study `scripts/` Python modules
2. ✅ Modify transformation rules
3. ✅ Add custom validations
4. ✅ Implement error handling
5. ✅ Set up monitoring

---

## 🔍 Where to Find What

### Want to...
- **Setup the system?** → `GETTING_STARTED.md` or `QUICKSTART.md`
- **Understand architecture?** → `PROJECT_SUMMARY.md`
- **Find a command?** → `COMMANDS.md`
- **Troubleshoot issues?** → `README.md` → Troubleshooting
- **Change email template?** → `scripts/email_utils.py`
- **Modify cleaning rules?** → `scripts/transform.py`
- **Change schedule?** → `dags/birthday_email_dag.py`
- **Update SMTP settings?** → `.env`
- **Add birthdays?** → `data/raw/birthdays.csv`
- **View processed data?** → `data/processed/cleaned_birthdays.csv`
- **Check logs?** → Airflow UI or `logs/` directory
- **Test components?** → Run `test_pipeline.py`

### Common File Edits
1. **Most Common**: `data/raw/birthdays.csv` (add birthdays)
2. **Setup**: `.env` (SMTP credentials)
3. **Customization**: `scripts/email_utils.py` (email template)
4. **Schedule**: `dags/birthday_email_dag.py` (timing)
5. **Rules**: `scripts/transform.py` (data validation)

---

## 🎯 Success Metrics

### System Health
- ✅ All Docker containers "healthy"
- ✅ Airflow UI accessible at http://localhost:8080
- ✅ DAG visible and enabled
- ✅ No errors in logs

### Functional Success
- ✅ Birthdays correctly extracted from CSV
- ✅ Data cleaned and validated
- ✅ Dates parsed correctly
- ✅ Today's birthdays detected
- ✅ Emails delivered successfully
- ✅ Summary statistics accurate

---

## 🆘 Quick Help References

### Something Broken?
1. **DAG not showing**: `COMMANDS.md` → Debugging
2. **Email not sending**: `README.md` → Troubleshooting → Email issues
3. **No birthdays found**: Check date format in CSV
4. **Docker issues**: Restart Docker Desktop

### Need to Learn?
1. **Airflow**: https://airflow.apache.org/docs/
2. **Pandas**: https://pandas.pydata.org/docs/
3. **Docker**: https://docs.docker.com/
4. **Python**: https://docs.python.org/3/

### Quick Commands
```powershell
# Start system
.\setup.ps1

# Stop system
.\stop.ps1

# View logs
docker-compose logs -f airflow-scheduler

# Restart scheduler
docker-compose restart airflow-scheduler

# Test pipeline
python test_pipeline.py
```

---

## 📞 Support Resources

### Documentation
1. **Getting Started**: `GETTING_STARTED.md`
2. **Quick Setup**: `QUICKSTART.md`
3. **Full Docs**: `README.md`
4. **Architecture**: `PROJECT_SUMMARY.md`
5. **Commands**: `COMMANDS.md`
6. **This Index**: `INDEX.md`

### Tools
- **Test Script**: `test_pipeline.py`
- **Setup Script**: `setup.ps1`
- **Stop Script**: `stop.ps1`

### URLs
- **Airflow UI**: http://localhost:8080
- **Login**: airflow / airflow

---

## 🎉 You're All Set!

This index should help you navigate the project. Start with `GETTING_STARTED.md` if you're new, or jump to `COMMANDS.md` for quick reference.

**Happy Birthday Scheduling! 🎂**

---

*Last Updated: December 2024*
*Version: 1.0.0*
*Project: Infosys Birthday Email Scheduler*
