# Birthday Email Scheduler

A Python-based Airflow DAG that automatically sends birthday emails to people on their special day.

## Features

- **Extract**: Reads birthday data from CSV files
- **Transform**: Cleans and validates data (removes duplicates, validates emails, parses dates)
- **Load**: Saves processed data for future reference
- **Check**: Identifies birthdays for the current day
- **Send**: Automatically sends personalized birthday emails

## Project Structure

```
Birthday_sch/
├── config/
│   └── config.yaml              # Configuration file
├── dags/
│   └── birthday_email_dag.py    # Main Airflow DAG
├── data/
│   ├── raw/
│   │   └── birthdays.csv        # Input data (names, emails, DOBs)
│   └── processed/
│       └── cleaned_birthdays.csv # Cleaned data
├── scripts/
│   ├── extract.py               # Data extraction module
│   ├── transform.py             # Data transformation module
│   ├── load.py                  # Data loading module
│   └── email_utils.py           # Email sending utilities
├── logs/                        # Airflow logs
├── plugins/                     # Custom Airflow plugins
├── docker-compose.yaml          # Docker Compose configuration
├── .env                         # Environment variables (SMTP credentials)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Docker Compose**
- At least **4GB RAM** available for Docker containers
- **Gmail account** (or other SMTP provider) for sending emails

## Setup Instructions

### 1. Clone or Download the Project

Place all files in your project directory: `d:\sam\Projects\Infosys\Birthday_sch`

### 2. Configure Email Settings

Edit the `.env` file with your email credentials:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
SMTP_MAIL_FROM=your_email@gmail.com
```

#### For Gmail Users:
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the generated 16-character password
3. Use the App Password as `SMTP_PASSWORD` in `.env`

### 3. Prepare Birthday Data

Edit `data/raw/birthdays.csv` with actual birthday data:

```csv
name,email,dob
John Doe,john.doe@example.com,1990-01-15
Jane Smith,jane.smith@example.com,1985-05-20
```

**Date Format**: Use `YYYY-MM-DD` format for dates.

### 4. Start Docker Services

Open PowerShell in the project directory and run:

```powershell
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs (optional)
docker-compose logs -f airflow-webserver
```

**Note**: First-time setup takes 2-3 minutes to initialize the database and create the admin user.

### 5. Access Airflow Web UI

1. Open browser: http://localhost:8080
2. Login credentials:
   - Username: `airflow`
   - Password: `airflow`

### 6. Enable and Run the DAG

1. Find `birthday_email_scheduler` in the DAG list
2. Toggle the DAG to **ON** (switch on the left)
3. Click the **Play button** (▶) to trigger manually
4. Or wait for the scheduled run at 9:00 AM daily

### 7. Monitor Execution

- Click on the DAG name to view details
- Use the **Graph** view to see task dependencies
- Click on individual tasks to view logs
- Check the **Log Summary** task for a daily report

## How It Works

### DAG Workflow

```
Extract Data → Transform Data → Check Birthdays → Send Emails → Log Summary
```

1. **Extract Data**: Reads `birthdays.csv` from the `data/raw/` directory
2. **Transform Data**: 
   - Removes duplicates
   - Validates email addresses
   - Parses dates and extracts month/day
   - Standardizes name formatting
3. **Check Birthdays**: Filters records where birth_month and birth_day match today's date
4. **Send Emails**: Sends personalized HTML birthday emails to matching recipients
5. **Log Summary**: Generates a report with statistics

### Schedule

- **Default**: Runs daily at 9:00 AM UTC
- **Cron Expression**: `0 9 * * *`
- **Timezone**: UTC (can be configured)

To change the schedule, edit the `schedule_interval` in `dags/birthday_email_dag.py`:

```python
schedule_interval='0 9 * * *',  # Daily at 9 AM
```

## Data Format

### Input CSV Format (`data/raw/birthdays.csv`)

```csv
name,email,dob
John Doe,john.doe@example.com,1990-01-15
Jane Smith,jane.smith@example.com,1985-05-20
```

**Required Columns:**
- `name`: Person's full name
- `email`: Valid email address
- `dob`: Date of birth in `YYYY-MM-DD` format

**Supported Date Formats:**
- `YYYY-MM-DD` (recommended)
- `DD/MM/YYYY`
- `MM/DD/YYYY`
- `DD-MM-YYYY`
- `MM-DD-YYYY`

## Testing

### Test with Today's Date

To test the system, add a record with today's date:

```csv
name,email,dob
Test User,your_test_email@example.com,2024-12-11
```

Replace `2024-12-11` with today's date.

### Manual Trigger

1. Go to Airflow UI (http://localhost:8080)
2. Find `birthday_email_scheduler`
3. Click the **Play** button
4. Select **Trigger DAG**
5. Monitor the execution in the Graph view

## Troubleshooting

### Issue: DAG Not Appearing in Airflow UI

**Solution:**
```powershell
# Check scheduler logs
docker-compose logs airflow-scheduler

# Restart scheduler
docker-compose restart airflow-scheduler
```

### Issue: Email Not Sending

**Possible Causes:**
1. **SMTP credentials not set**: Check `.env` file
2. **Invalid App Password**: Generate a new one
3. **Gmail security**: Ensure 2FA is enabled and App Password is used

**Debug:**
```powershell
# Check webserver logs
docker-compose logs airflow-webserver

# View task logs in Airflow UI
# Click on task → Logs
```

### Issue: Date Parsing Errors

**Solution:**
- Ensure dates are in supported format: `YYYY-MM-DD`
- Check for extra spaces or special characters
- View transform task logs for specific errors

### Issue: No Birthdays Found

**Check:**
1. Verify current date matches records in CSV
2. Check transformation logs for data cleaning issues
3. Ensure dates were parsed correctly (check `birth_month` and `birth_day` columns)

## Stopping the System

```powershell
# Stop all services (data persists)
docker-compose stop

# Stop and remove containers (data persists in volumes)
docker-compose down

# Stop and remove everything including data
docker-compose down -v
```

## Useful Commands

### Docker Commands

```powershell
# View all running containers
docker-compose ps

# View logs for specific service
docker-compose logs -f airflow-webserver
docker-compose logs -f airflow-scheduler

# Execute command in container
docker-compose exec airflow-webserver bash

# Restart specific service
docker-compose restart airflow-scheduler

# Check container resource usage
docker stats
```

### Airflow Commands

```powershell
# List all DAGs
docker-compose exec airflow-webserver airflow dags list

# Test a specific task
docker-compose exec airflow-webserver airflow tasks test birthday_email_scheduler extract_data 2024-12-11

# Create new user
docker-compose exec airflow-webserver airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

## Customization

### Change Email Template

Edit `scripts/email_utils.py` → `create_birthday_email()` method to customize:
- Email subject
- HTML template
- Plain text version

### Add More Data Validation

Edit `scripts/transform.py` → `BirthdayDataCleaner` class to add:
- Phone number validation
- Address validation
- Custom business rules

### Change Schedule

Edit `dags/birthday_email_dag.py`:

```python
# Run every hour
schedule_interval='0 * * * *'

# Run every Monday at 10 AM
schedule_interval='0 10 * * 1'

# Run on specific days
schedule_interval='0 9 1,15 * *'  # 1st and 15th of each month
```

## Dependencies

Key Python packages:
- `apache-airflow==2.8.0` - Workflow orchestration
- `pandas>=2.0.0` - Data manipulation
- `openpyxl>=3.1.0` - Excel support
- `python-dotenv` - Environment variable management

See `requirements.txt` for complete list.

## Security Notes

1. **Never commit `.env` file** to version control
2. Use **App Passwords** instead of account passwords
3. Consider using **Airflow Connections** for production environments
4. Restrict access to Airflow UI in production

## Support

For issues:
1. Check logs: `docker-compose logs -f`
2. View task logs in Airflow UI
3. Verify email configuration in `.env`
4. Test date parsing with sample data

## License

MIT License - Feel free to modify and use for your needs.

## Author

Created for Infosys Birthday Scheduler Project

## Acknowledgments

- Based on Apache Airflow ETL framework
- Email templates inspired by modern HTML email designs
- Docker configuration adapted from official Airflow documentation
