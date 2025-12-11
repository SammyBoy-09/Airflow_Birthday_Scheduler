"""
Email utility module for sending birthday emails.
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailSender:
    """Class for sending birthday emails."""
    
    def __init__(self, smtp_host: str, smtp_port: int, smtp_user: str, smtp_password: str, from_email: str):
        """
        Initialize email sender.
        
        Args:
            smtp_host: SMTP server host
            smtp_port: SMTP server port
            smtp_user: SMTP username
            smtp_password: SMTP password
            from_email: Sender email address
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_email = from_email
    
    def create_birthday_email(self, name: str, to_email: str) -> MIMEMultipart:
        """
        Create a birthday email message.
        
        Args:
            name: Recipient's name
            to_email: Recipient's email address
            
        Returns:
            Email message object
        """
        message = MIMEMultipart('alternative')
        message['Subject'] = f'🎉 Happy Birthday {name}!'
        message['From'] = self.from_email
        message['To'] = to_email
        
        # Plain text version
        text = f"""
        Happy Birthday {name}! 🎂
        
        Wishing you a fantastic day filled with joy, laughter, and all the things you love!
        
        May this year bring you success, happiness, and countless memorable moments.
        
        Warm wishes,
        Samuel Lazar
        """
        
        # HTML version
        html = f"""
        <html>
          <head></head>
          <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
              <h1 style="color: #FF6B6B; text-align: center;">🎉 Happy Birthday {name}! 🎉</h1>
              <div style="margin: 30px 0; text-align: center;">
                <img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMHE3d25jdHBneXFkZ3dvNW9tOTJ0djlzcGtzc3g3NXFqMGJmYnQyaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6WFScxN6fi95z3YVQD/giphy.gif" alt="Birthday Cake" style="max-width: 300px; border-radius: 10px;">
              </div>
              <p style="font-size: 16px; line-height: 1.6; color: #333;">
                Wishing you a <strong>fantastic day</strong> filled with joy, laughter, and all the things you love!
              </p>
              <p style="font-size: 16px; line-height: 1.6; color: #333;">
                May this year bring you success, happiness, and countless memorable moments. 🌟
              </p>
              <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #FF6B6B; text-align: center; color: #666;">
                <p>Warm wishes,<br><strong>Samuel Lazar</strong></p>
              </div>
            </div>
          </body>
        </html>
        """
        
        # Attach both versions
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        message.attach(part1)
        message.attach(part2)
        
        return message
    
    def send_email(self, message: MIMEMultipart) -> bool:
        """
        Send an email message.
        
        Args:
            message: Email message to send
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Connecting to SMTP server: {self.smtp_host}:{self.smtp_port}")
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()  # Enable TLS
                server.login(self.smtp_user, self.smtp_password)
                
                # Send the email
                server.send_message(message)
                
                logger.info(f"Successfully sent email to {message['To']}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to send email to {message['To']}: {str(e)}")
            return False
    
    def send_birthday_emails(self, birthday_people: List[Dict]) -> Dict[str, int]:
        """
        Send birthday emails to multiple recipients.
        
        Args:
            birthday_people: List of dictionaries with 'name' and 'email' keys
            
        Returns:
            Dictionary with success and failure counts
        """
        results = {'success': 0, 'failed': 0}
        
        logger.info(f"Preparing to send {len(birthday_people)} birthday emails")
        
        for person in birthday_people:
            name = person.get('name', 'Friend')
            email = person.get('email')
            
            if not email:
                logger.warning(f"No email address for {name}, skipping")
                results['failed'] += 1
                continue
            
            try:
                message = self.create_birthday_email(name, email)
                if self.send_email(message):
                    results['success'] += 1
                else:
                    results['failed'] += 1
            except Exception as e:
                logger.error(f"Error processing email for {name}: {str(e)}")
                results['failed'] += 1
        
        logger.info(f"Email sending complete. Success: {results['success']}, Failed: {results['failed']}")
        return results


def send_birthday_emails_task(birthday_people: List[Dict], 
                               smtp_host: str,
                               smtp_port: int,
                               smtp_user: str,
                               smtp_password: str,
                               from_email: str) -> Dict[str, int]:
    """
    Wrapper function for Airflow task.
    
    Args:
        birthday_people: List of people with birthdays today
        smtp_host: SMTP server host
        smtp_port: SMTP server port
        smtp_user: SMTP username
        smtp_password: SMTP password
        from_email: Sender email address
        
    Returns:
        Results dictionary with counts
    """
    sender = EmailSender(smtp_host, smtp_port, smtp_user, smtp_password, from_email)
    return sender.send_birthday_emails(birthday_people)


if __name__ == "__main__":
    # Test the email sender
    import os
    
    # Test data
    test_people = [
        {'name': 'John Doe', 'email': 'test@example.com'}
    ]
    
    # Get credentials from environment or use placeholders
    sender = EmailSender(
        smtp_host=os.getenv('SMTP_HOST', 'smtp.gmail.com'),
        smtp_port=int(os.getenv('SMTP_PORT', 587)),
        smtp_user=os.getenv('SMTP_USER', 'your_email@gmail.com'),
        smtp_password=os.getenv('SMTP_PASSWORD', 'your_password'),
        from_email=os.getenv('SMTP_MAIL_FROM', 'your_email@gmail.com')
    )
    
    print("Email sender initialized. Update .env file with actual credentials to test.")
