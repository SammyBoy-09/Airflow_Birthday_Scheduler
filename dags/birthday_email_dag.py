"""
Birthday Email Scheduler DAG

This DAG runs daily to:
1. Extract birthday data from a CSV file
2. Transform and clean the data
3. Check if today is anyone's birthday
4. Send birthday emails to those people
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import os
import sys
import logging
import pendulum

# Add scripts directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.extract import extract
from scripts.transform import transform
from scripts.load import load
from scripts.email_utils import send_birthday_emails_task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set timezone to IST (Indian Standard Time)
IST = pendulum.timezone('Asia/Kolkata')

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1, tzinfo=IST),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
# Note: timezone is set via start_date tzinfo in default_args for Airflow 2.8.0
dag = DAG(
    'birthday_email_scheduler',
    default_args=default_args,
    description='Daily birthday email scheduler that extracts, transforms, and sends birthday emails (IST timezone)',
    schedule_interval='0 9 * * *',  # Run daily at 9:00 AM IST
    catchup=False,
    tags=['birthday', 'email', 'etl'],
)


def extract_birthday_data(**context):
    """
    Task 1: Extract birthday data from CSV file.
    """
    logger.info("Starting data extraction")
    
    # Define file path
    input_file = '/opt/airflow/data/raw/birthdays.csv'
    
    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Extract data
    df = extract(input_file)
    
    # Save to XCom for next task
    output_file = '/opt/airflow/data/raw/extracted_birthdays.csv'
    df.to_csv(output_file, index=False)
    
    logger.info(f"Extracted {len(df)} records")
    context['ti'].xcom_push(key='extracted_file', value=output_file)
    context['ti'].xcom_push(key='record_count', value=len(df))
    
    return output_file


def transform_birthday_data(**context):
    """
    Task 2: Transform and clean the birthday data.
    """
    logger.info("Starting data transformation")
    
    # Get extracted file from previous task
    ti = context['ti']
    input_file = ti.xcom_pull(key='extracted_file', task_ids='extract_data')
    
    # Read the data
    df = pd.read_csv(input_file)
    
    # Transform the data
    df_cleaned = transform(df)
    
    # Save cleaned data
    output_file = '/opt/airflow/data/processed/cleaned_birthdays.csv'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df_cleaned.to_csv(output_file, index=False)
    
    logger.info(f"Transformed data: {len(df_cleaned)} records after cleaning")
    ti.xcom_push(key='cleaned_file', value=output_file)
    ti.xcom_push(key='cleaned_count', value=len(df_cleaned))
    
    return output_file


def check_todays_birthdays(**context):
    """
    Task 3: Check if today is anyone's birthday and prepare email list.
    """
    logger.info("Checking for today's birthdays")
    
    # Get cleaned file from previous task
    ti = context['ti']
    input_file = ti.xcom_pull(key='cleaned_file', task_ids='transform_data')
    
    # Read cleaned data
    df = pd.read_csv(input_file)
    
    # Get today's date
    today = datetime.now()
    current_month = today.month
    current_day = today.day
    
    logger.info(f"Today's date: {today.strftime('%Y-%m-%d')} (Month: {current_month}, Day: {current_day})")
    
    # Filter for today's birthdays
    if 'birth_month' in df.columns and 'birth_day' in df.columns:
        todays_birthdays = df[
            (df['birth_month'] == current_month) & 
            (df['birth_day'] == current_day)
        ]
    else:
        logger.error("Required columns 'birth_month' and 'birth_day' not found")
        todays_birthdays = pd.DataFrame()
    
    logger.info(f"Found {len(todays_birthdays)} birthday(s) today")
    
    # Prepare birthday list for email sending
    birthday_list = []
    if len(todays_birthdays) > 0:
        for _, row in todays_birthdays.iterrows():
            birthday_list.append({
                'name': row['name'],
                'email': row['email']
            })
            logger.info(f"Birthday today: {row['name']} ({row['email']})")
    
    # Save to XCom
    ti.xcom_push(key='birthday_list', value=birthday_list)
    ti.xcom_push(key='birthday_count', value=len(birthday_list))
    
    return birthday_list


def send_birthday_emails(**context):
    """
    Task 4: Send birthday emails to people with birthdays today.
    """
    logger.info("Starting email sending task")
    
    # Get birthday list from previous task
    ti = context['ti']
    birthday_list = ti.xcom_pull(key='birthday_list', task_ids='check_birthdays')
    
    if not birthday_list or len(birthday_list) == 0:
        logger.info("No birthdays today. No emails to send.")
        return {'success': 0, 'failed': 0, 'message': 'No birthdays today'}
    
    # Get email configuration from environment
    smtp_host = os.getenv('AIRFLOW__SMTP__SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.getenv('AIRFLOW__SMTP__SMTP_PORT', 587))
    smtp_user = os.getenv('AIRFLOW__SMTP__SMTP_USER', '')
    smtp_password = os.getenv('AIRFLOW__SMTP__SMTP_PASSWORD', '')
    from_email = os.getenv('AIRFLOW__SMTP__SMTP_MAIL_FROM', smtp_user)
    
    # Validate email configuration
    if not smtp_user or not smtp_password:
        logger.error("SMTP credentials not configured. Please set SMTP environment variables.")
        logger.info("Emails would have been sent to:")
        for person in birthday_list:
            logger.info(f"  - {person['name']} ({person['email']})")
        return {'success': 0, 'failed': len(birthday_list), 'message': 'SMTP not configured'}
    
    # Send emails
    results = send_birthday_emails_task(
        birthday_people=birthday_list,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        smtp_user=smtp_user,
        smtp_password=smtp_password,
        from_email=from_email
    )
    
    logger.info(f"Email sending complete: {results}")
    ti.xcom_push(key='email_results', value=results)
    
    return results


def log_summary(**context):
    """
    Task 5: Log a summary of the entire process.
    """
    logger.info("Generating summary report")
    
    ti = context['ti']
    
    # Pull data from previous tasks
    record_count = ti.xcom_pull(key='record_count', task_ids='extract_data')
    cleaned_count = ti.xcom_pull(key='cleaned_count', task_ids='transform_data')
    birthday_count = ti.xcom_pull(key='birthday_count', task_ids='check_birthdays')
    birthday_list = ti.xcom_pull(key='birthday_list', task_ids='check_birthdays')
    email_results = ti.xcom_pull(key='email_results', task_ids='send_emails')
    
    # Build recipients list
    recipients_text = ""
    if birthday_list and len(birthday_list) > 0:
        recipients_text = "\n    BIRTHDAY RECIPIENTS:\n"
        for i, person in enumerate(birthday_list, 1):
            recipients_text += f"    {i}. {person.get('name', 'Unknown')} ({person.get('email', 'No email')})\n"
    else:
        recipients_text = "\n    No birthdays today.\n"
    
    # Create summary
    summary = f"""
    ========================================
    BIRTHDAY EMAIL SCHEDULER - DAILY REPORT
    ========================================
    Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    EXTRACTION:
    - Records extracted: {record_count}
    
    TRANSFORMATION:
    - Records after cleaning: {cleaned_count}
    - Records removed: {record_count - cleaned_count if record_count and cleaned_count else 0}
    
    BIRTHDAY CHECK:
    - Birthdays today: {birthday_count}
{recipients_text}
    EMAIL SENDING:
    - Emails sent successfully: {email_results.get('success', 0) if email_results else 0}
    - Emails failed: {email_results.get('failed', 0) if email_results else 0}
    
    ========================================
    """
    
    logger.info(summary)
    print(summary)
    
    return summary


# Define tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_birthday_data,
    provide_context=True,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_birthday_data,
    provide_context=True,
    dag=dag,
)

check_birthdays_task = PythonOperator(
    task_id='check_birthdays',
    python_callable=check_todays_birthdays,
    provide_context=True,
    dag=dag,
)

send_emails_task = PythonOperator(
    task_id='send_emails',
    python_callable=send_birthday_emails,
    provide_context=True,
    dag=dag,
)

summary_task = PythonOperator(
    task_id='log_summary',
    python_callable=log_summary,
    provide_context=True,
    dag=dag,
)

# Define task dependencies
extract_task >> transform_task >> check_birthdays_task >> send_emails_task >> summary_task
