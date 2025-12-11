"""
__init__.py for scripts package
This makes the scripts directory a Python package.
"""

# Version info
__version__ = '1.0.0'
__author__ = 'Infosys Birthday Scheduler Team'

# Import main functions for easier access
from .extract import extract
from .transform import transform
from .load import load
from .email_utils import EmailSender, send_birthday_emails_task

__all__ = [
    'extract',
    'transform',
    'load',
    'EmailSender',
    'send_birthday_emails_task',
]
