"""
Test script to validate the ETL pipeline components.
Run this before deploying to Airflow to ensure everything works.
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

import pandas as pd
from datetime import datetime

print("="*60)
print("BIRTHDAY SCHEDULER - COMPONENT TEST")
print("="*60)

# Test 1: Import modules
print("\n[1/5] Testing module imports...")
try:
    from scripts.extract import extract
    from scripts.transform import transform
    from scripts.load import load
    from scripts.email_utils import EmailSender
    print("✓ All modules imported successfully")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Extract
print("\n[2/5] Testing data extraction...")
try:
    input_file = "data/raw/birthdays.csv"
    if not os.path.exists(input_file):
        print(f"✗ File not found: {input_file}")
        sys.exit(1)
    
    df = extract(input_file)
    print(f"✓ Extracted {len(df)} records")
    print(f"  Columns: {list(df.columns)}")
except Exception as e:
    print(f"✗ Extract failed: {e}")
    sys.exit(1)

# Test 3: Transform
print("\n[3/5] Testing data transformation...")
try:
    df_cleaned = transform(df)
    print(f"✓ Transformed data: {len(df_cleaned)} records after cleaning")
    print(f"  Columns: {list(df_cleaned.columns)}")
    
    if 'birth_month' in df_cleaned.columns and 'birth_day' in df_cleaned.columns:
        print("✓ Date parsing successful")
    else:
        print("✗ Date parsing failed - missing birth_month/birth_day columns")
except Exception as e:
    print(f"✗ Transform failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Load
print("\n[4/5] Testing data loading...")
try:
    output_file = "data/processed/test_cleaned_birthdays.csv"
    load(df_cleaned, csv_path=output_file)
    print(f"✓ Data saved to {output_file}")
except Exception as e:
    print(f"✗ Load failed: {e}")
    sys.exit(1)

# Test 5: Check birthdays
print("\n[5/5] Testing birthday detection...")
try:
    today = datetime.now()
    current_month = today.month
    current_day = today.day
    
    print(f"  Today's date: {today.strftime('%Y-%m-%d')} (Month: {current_month}, Day: {current_day})")
    
    todays_birthdays = df_cleaned[
        (df_cleaned['birth_month'] == current_month) & 
        (df_cleaned['birth_day'] == current_day)
    ]
    
    print(f"✓ Found {len(todays_birthdays)} birthday(s) today")
    
    if len(todays_birthdays) > 0:
        print("\n  🎂 Birthday(s) today:")
        for _, row in todays_birthdays.iterrows():
            print(f"     - {row['name']} ({row['email']})")
        
        # Test email creation (but don't send)
        print("\n  Testing email creation (not sending)...")
        sender = EmailSender(
            smtp_host='smtp.gmail.com',
            smtp_port=587,
            smtp_user='test@example.com',
            smtp_password='dummy',
            from_email='test@example.com'
        )
        
        for _, row in todays_birthdays.iterrows():
            message = sender.create_birthday_email(row['name'], row['email'])
            print(f"     ✓ Created email for {row['name']}")
    else:
        print("  ℹ No birthdays today. Add a record with today's date to test email.")
        print(f"     Example: Test User,test@example.com,{today.strftime('%Y-%m-%d')}")
    
except Exception as e:
    print(f"✗ Birthday check failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("\n" + "="*60)
print("✅ ALL TESTS PASSED")
print("="*60)
print("\nNext steps:")
print("1. Update .env with your SMTP credentials")
print("2. Start Docker: docker-compose up -d")
print("3. Access Airflow UI: http://localhost:8080")
print("4. Enable and trigger the birthday_email_scheduler DAG")
print("\nFor immediate test, add a birthday with today's date to birthdays.csv")
print("="*60)
