# Quick Start Guide - Birthday Email Scheduler

## 🚀 Quick Setup (5 Minutes)

### Step 1: Configure Email (2 min)

1. Open `.env` file
2. Update these values:
   ```
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_16_char_app_password
   SMTP_MAIL_FROM=your_email@gmail.com
   ```

**Get Gmail App Password:**
- Visit: https://myaccount.google.com/apppasswords
- Enable 2FA first if not already enabled
- Generate password for "Mail" → Copy the 16-character password

### Step 2: Add Birthday Data (1 min)

1. Open `data/raw/birthdays.csv`
2. Add real data or test with today's date:
   ```csv
   name,email,dob
   Your Name,your.email@example.com,2024-12-11
   ```
   (Replace date with TODAY's date for testing)

### Step 3: Start Docker (2 min)

```powershell
# In project directory
docker-compose up -d

# Wait 2-3 minutes for initialization
docker-compose ps
```

### Step 4: Run DAG

1. Open: http://localhost:8080
2. Login: `airflow` / `airflow`
3. Toggle **birthday_email_scheduler** to ON
4. Click ▶ (Play button) → Trigger DAG
5. Watch it run in Graph view!

## ✅ Quick Test

To test immediately, add this line to `birthdays.csv`:
```csv
Test User,your.test.email@gmail.com,2024-12-11
```
Replace `2024-12-11` with **today's date** and use your real email.

## 🎯 Expected Results

If today matches a birthday in the CSV:
- ✅ Extract: Reads CSV
- ✅ Transform: Cleans data
- ✅ Check: Finds birthday match
- ✅ Send: Sends email
- ✅ Summary: Shows statistics

Check your email inbox! 📧

## 🔍 View Logs

Click any task box → Click "Logs" button

## 🛑 Stop System

```powershell
docker-compose down
```

## 📚 Full Documentation

See `README.md` for complete details, troubleshooting, and customization.

## 🆘 Common Issues

**DAG not showing?**
```powershell
docker-compose restart airflow-scheduler
```

**Email not sending?**
- Check `.env` has correct App Password
- Verify 2FA is enabled on Gmail
- Check logs in Airflow UI

**No birthdays found?**
- Verify CSV date matches today's date
- Check date format is YYYY-MM-DD

## 📞 Quick Commands

```powershell
# View logs
docker-compose logs -f airflow-webserver

# Restart services
docker-compose restart airflow-scheduler

# Stop everything
docker-compose down
```

## 🎉 Success!

If you received an email, congratulations! The system is working.

Now update `birthdays.csv` with real data and let it run automatically every day at 9 AM.
