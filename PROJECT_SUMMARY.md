# PROJECT SUMMARY - Birthday Email Scheduler

## 📁 Complete File Structure

```
Birthday_sch/
├── config/
│   └── config.yaml              # Configuration settings
│
├── dags/
│   └── birthday_email_dag.py    # Main Airflow DAG (orchestrates the workflow)
│
├── data/
│   ├── raw/
│   │   └── birthdays.csv        # Input: Names, emails, DOBs
│   └── processed/
│       └── .gitkeep             # Cleaned data output location
│
├── logs/                        # Airflow execution logs
│
├── plugins/                     # Custom Airflow plugins (extensibility)
│   └── .gitkeep
│
├── scripts/
│   ├── extract.py               # ETL: Extract data from CSV/Excel
│   ├── transform.py             # ETL: Clean and validate data
│   ├── load.py                  # ETL: Save processed data
│   └── email_utils.py           # Send birthday emails via SMTP
│
├── .env                         # SMTP credentials (DO NOT COMMIT)
├── .gitignore                   # Git ignore rules
├── docker-compose.yaml          # Docker orchestration (Airflow + PostgreSQL)
├── README.md                    # Full documentation
├── QUICKSTART.md                # 5-minute setup guide
├── requirements.txt             # Python dependencies
├── setup.ps1                    # Automated setup script
├── stop.ps1                     # Service stop script
└── test_pipeline.py             # Component testing script

```

## 🔄 Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    DAILY AT 9:00 AM                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  1. EXTRACT DATA                                            │
│  ─────────────────────────────────────────────────────      │
│  • Read birthdays.csv from data/raw/                        │
│  • Load into pandas DataFrame                               │
│  • Pass to next task via XCom                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  2. TRANSFORM DATA                                          │
│  ─────────────────────────────────────────────────────────  │
│  • Remove leading/trailing whitespace                       │
│  • Validate email addresses                                 │
│  • Parse dates (multiple formats supported)                 │
│  • Extract birth month and day                              │
│  • Remove duplicates                                        │
│  • Drop invalid/missing data                                │
│  • Standardize name formatting                              │
│  • Save cleaned data to data/processed/                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  3. CHECK BIRTHDAYS                                         │
│  ─────────────────────────────────────────────────────────  │
│  • Get current date (month + day)                           │
│  • Filter records where birth_month = current_month         │
│    AND birth_day = current_day                              │
│  • Create list of birthday people                           │
│  • Pass list to email task                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  4. SEND EMAILS                                             │
│  ─────────────────────────────────────────────────────────  │
│  • For each person with birthday today:                     │
│    - Create personalized HTML email                         │
│    - Connect to SMTP server (Gmail)                         │
│    - Send birthday email                                    │
│  • Track success/failure counts                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  5. LOG SUMMARY                                             │
│  ─────────────────────────────────────────────────────────  │
│  • Display statistics:                                      │
│    - Records extracted                                      │
│    - Records after cleaning                                 │
│    - Birthdays today                                        │
│    - Emails sent (success/failed)                           │
└─────────────────────────────────────────────────────────────┘
```

## 🧩 Component Details

### 1. Docker Compose (`docker-compose.yaml`)
**Purpose**: Orchestrates all services
**Services**:
- PostgreSQL: Stores Airflow metadata and task history
- Airflow Webserver: Web UI on port 8080
- Airflow Scheduler: Executes DAGs on schedule
- Airflow Init: Initializes database and creates admin user

**Volumes**:
- Mounts local directories into containers
- Enables code changes without rebuilding

### 2. Airflow DAG (`dags/birthday_email_dag.py`)
**Purpose**: Defines the workflow and task dependencies
**Schedule**: `0 9 * * *` (Daily at 9 AM)
**Tasks**:
1. `extract_data` → Extract from CSV
2. `transform_data` → Clean and validate
3. `check_birthdays` → Filter today's birthdays
4. `send_emails` → Send birthday emails
5. `log_summary` → Generate report

**Key Features**:
- XCom for passing data between tasks
- Error handling and logging
- Configurable via environment variables

### 3. Extract Module (`scripts/extract.py`)
**Purpose**: Read data from various sources
**Supports**:
- CSV files
- Excel files (.xlsx, .xls)
- Auto-detects file type from extension
**Output**: pandas DataFrame

### 4. Transform Module (`scripts/transform.py`)
**Purpose**: Clean and validate data
**Operations**:
- Trim whitespace
- Email validation (regex)
- Date parsing (multiple formats)
- Duplicate removal
- Missing data handling
- Name standardization
**Output**: Cleaned DataFrame with birth_month and birth_day columns

### 5. Load Module (`scripts/load.py`)
**Purpose**: Save processed data
**Supports**:
- CSV export
- Excel export
**Creates directories if needed**

### 6. Email Utils (`scripts/email_utils.py`)
**Purpose**: Send birthday emails
**Features**:
- HTML email with styling
- Plain text fallback
- SMTP with TLS encryption
- Batch sending
- Error tracking
**Configuration**: Uses environment variables from `.env`

### 7. Environment File (`.env`)
**Purpose**: Store sensitive credentials
**Contains**:
- SMTP_HOST: Email server
- SMTP_PORT: Server port (587 for TLS)
- SMTP_USER: Email username
- SMTP_PASSWORD: Email password (App Password for Gmail)
- SMTP_MAIL_FROM: Sender email

⚠️ **NEVER commit this file to Git**

## 🔧 Configuration

### Schedule
Edit `schedule_interval` in `birthday_email_dag.py`:
```python
schedule_interval='0 9 * * *',  # Daily at 9 AM
```

### Email Template
Edit `create_birthday_email()` in `scripts/email_utils.py`

### Data Validation Rules
Edit `BirthdayDataCleaner` methods in `scripts/transform.py`

### Timezone
Set in DAG or Airflow configuration (default: UTC)

## 📊 Data Flow

```
birthdays.csv (raw)
    ↓ [Extract]
DataFrame (in memory)
    ↓ [Transform]
cleaned_birthdays.csv (processed)
    ↓ [Check]
birthday_list (XCom)
    ↓ [Send]
Emails sent to recipients
    ↓ [Log]
Summary statistics logged
```

## 🔐 Security Considerations

1. **Gmail App Password**: Use 2FA + App Password (not account password)
2. **Environment Variables**: Never commit `.env` to Git
3. **Airflow UI**: In production, change default credentials
4. **Email Validation**: Prevents sending to invalid addresses
5. **Data Privacy**: Consider GDPR/privacy laws for birthday data

## 🚀 Deployment Options

### Option 1: Local Development (Current Setup)
- Docker on local machine
- Airflow UI on localhost:8080
- Good for testing and small teams

### Option 2: Production Server
- Deploy on Linux server
- Use reverse proxy (Nginx) for HTTPS
- Set up proper authentication
- Use managed database instead of PostgreSQL container
- Set up monitoring and alerting

### Option 3: Cloud Deployment
- AWS: Use Amazon MWAA (Managed Airflow)
- GCP: Use Cloud Composer
- Azure: Use Azure Data Factory or Airflow on AKS

## 📈 Scaling Considerations

**Current Setup**: LocalExecutor (single machine)
**For More Tasks**: Use CeleryExecutor with Redis/RabbitMQ
**For Large Data**: Add data partitioning and parallel processing
**For High Availability**: Use Kubernetes with multiple scheduler replicas

## 🧪 Testing Strategy

1. **Unit Tests**: Test individual functions in scripts
2. **Integration Tests**: Test task execution
3. **End-to-End Tests**: Full DAG run with test data
4. **Manual Testing**: Use `test_pipeline.py`

## 📋 Maintenance Tasks

### Daily
- Monitor DAG runs in Airflow UI
- Check email delivery success rates

### Weekly
- Review logs for errors
- Verify data quality
- Update birthday data

### Monthly
- Update dependencies: `pip install -U -r requirements.txt`
- Clean old logs: `docker-compose exec airflow-scheduler airflow db clean`
- Backup PostgreSQL database

### As Needed
- Rotate SMTP credentials
- Update email templates
- Add new features

## 🐛 Troubleshooting Resources

1. **Airflow Logs**: Check in UI or `logs/` directory
2. **Docker Logs**: `docker-compose logs -f [service]`
3. **Task Logs**: Click task in UI → Logs button
4. **Test Script**: Run `python test_pipeline.py`
5. **PostgreSQL**: Access with `docker-compose exec postgres psql -U airflow`

## 📚 Learning Resources

- Airflow Docs: https://airflow.apache.org/docs/
- Pandas Docs: https://pandas.pydata.org/docs/
- Docker Docs: https://docs.docker.com/
- Gmail SMTP: https://support.google.com/mail/answer/7126229

## 🎯 Success Criteria

✅ Docker services running
✅ Airflow UI accessible
✅ DAG visible and enabled
✅ Tasks execute without errors
✅ Birthdays detected correctly
✅ Emails delivered successfully
✅ Logs show summary statistics

## 🔄 Future Enhancements

Potential improvements:
1. **Database Integration**: Read birthdays from PostgreSQL/MySQL
2. **Web Interface**: Add form to submit birthdays
3. **SMS Notifications**: Add SMS support via Twilio
4. **Slack Integration**: Post to Slack channel
5. **Timezone Support**: Handle multiple timezones
6. **Attachment Support**: Add birthday card images
7. **A/B Testing**: Test different email templates
8. **Analytics**: Track open rates and engagement
9. **Reminder Emails**: Send reminder before birthday
10. **Holiday Integration**: Skip sending on holidays

## 💡 Tips for Success

1. **Start Simple**: Test with one record first
2. **Use Today's Date**: For immediate testing
3. **Check Logs**: Always review logs after runs
4. **Backup Data**: Keep backup of birthdays.csv
5. **Document Changes**: Track customizations
6. **Monitor Performance**: Watch resource usage
7. **Regular Updates**: Keep dependencies current
8. **Security First**: Never expose credentials

## 🏆 Best Practices

1. **Version Control**: Use Git (exclude .env)
2. **Documentation**: Update README for changes
3. **Testing**: Test before deploying
4. **Monitoring**: Set up alerts for failures
5. **Backup**: Regular backups of data and config
6. **Security**: Rotate credentials regularly
7. **Code Quality**: Follow PEP 8 for Python
8. **Logging**: Use appropriate log levels

## 📞 Support

For issues:
1. Check QUICKSTART.md for common problems
2. Review README.md troubleshooting section
3. Check Airflow logs for error details
4. Test components with test_pipeline.py
5. Verify Docker services are running

---

**Project Created**: December 2024
**Author**: Infosys Birthday Scheduler Team
**License**: MIT
**Version**: 1.0.0
