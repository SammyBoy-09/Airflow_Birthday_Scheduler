"""
Transform module for cleaning and transforming birthday data.
"""
import pandas as pd
import numpy as np
import logging
import re
from datetime import datetime
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BirthdayDataCleaner:
    """Class for cleaning and transforming birthday data."""
    
    @staticmethod
    def trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
        """Remove leading and trailing whitespace from string columns."""
        logger.info("Trimming whitespace from string columns")
        string_columns = df.select_dtypes(include=['object']).columns
        for col in string_columns:
            df[col] = df[col].str.strip() if df[col].dtype == 'object' else df[col]
        return df
    
    @staticmethod
    def validate_email(df: pd.DataFrame, email_col: str = 'email', drop_invalid: bool = False) -> pd.DataFrame:
        """
        Validate email addresses.
        
        Args:
            df: DataFrame containing email column
            email_col: Name of the email column
            drop_invalid: Whether to drop invalid emails or mark them
            
        Returns:
            Cleaned DataFrame
        """
        logger.info(f"Validating email addresses in column '{email_col}'")
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if email_col not in df.columns:
            logger.warning(f"Column '{email_col}' not found in DataFrame")
            return df
        
        # Create a mask for valid emails
        valid_emails = df[email_col].apply(lambda x: bool(re.match(email_pattern, str(x))) if pd.notna(x) else False)
        
        invalid_count = (~valid_emails).sum()
        logger.info(f"Found {invalid_count} invalid email addresses")
        
        if drop_invalid:
            df = df[valid_emails].copy()
            logger.info(f"Dropped {invalid_count} rows with invalid emails")
        else:
            df['email_valid'] = valid_emails
        
        return df
    
    @staticmethod
    def parse_dob(df: pd.DataFrame, dob_col: str = 'dob') -> pd.DataFrame:
        """
        Parse date of birth and extract useful fields.
        
        Args:
            df: DataFrame containing DOB column
            dob_col: Name of the DOB column
            
        Returns:
            DataFrame with parsed DOB fields
        """
        logger.info(f"Parsing dates from column '{dob_col}'")
        
        if dob_col not in df.columns:
            logger.warning(f"Column '{dob_col}' not found in DataFrame")
            return df
        
        # Try multiple date formats
        date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y']
        
        def parse_date(date_str):
            if pd.isna(date_str):
                return None
            for fmt in date_formats:
                try:
                    return pd.to_datetime(date_str, format=fmt)
                except:
                    continue
            # If none of the formats work, try pandas auto-parsing
            try:
                return pd.to_datetime(date_str)
            except:
                return None
        
        # Parse dates
        df['dob_parsed'] = df[dob_col].apply(parse_date)
        
        # Extract month and day for birthday matching
        df['birth_month'] = df['dob_parsed'].dt.month
        df['birth_day'] = df['dob_parsed'].dt.day
        
        # Count parsing failures
        parse_failures = df['dob_parsed'].isna().sum()
        if parse_failures > 0:
            logger.warning(f"Failed to parse {parse_failures} dates")
        
        return df
    
    @staticmethod
    def remove_duplicates(df: pd.DataFrame, subset: Optional[list] = None) -> pd.DataFrame:
        """
        Remove duplicate rows.
        
        Args:
            df: DataFrame to clean
            subset: Columns to consider for duplicates (default: email)
            
        Returns:
            DataFrame without duplicates
        """
        if subset is None:
            subset = ['email']
        
        logger.info(f"Removing duplicates based on columns: {subset}")
        initial_count = len(df)
        df = df.drop_duplicates(subset=subset, keep='first')
        removed_count = initial_count - len(df)
        logger.info(f"Removed {removed_count} duplicate rows")
        
        return df
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset."""
        logger.info("Handling missing values")
        
        # Drop rows with missing critical fields
        critical_fields = ['name', 'email', 'dob']
        existing_critical = [field for field in critical_fields if field in df.columns]
        
        initial_count = len(df)
        df = df.dropna(subset=existing_critical)
        removed_count = initial_count - len(df)
        
        if removed_count > 0:
            logger.warning(f"Dropped {removed_count} rows with missing critical fields")
        
        return df
    
    @staticmethod
    def standardize_names(df: pd.DataFrame, name_col: str = 'name') -> pd.DataFrame:
        """Standardize name formatting."""
        logger.info(f"Standardizing names in column '{name_col}'")
        
        if name_col not in df.columns:
            return df
        
        # Title case for names
        df[name_col] = df[name_col].str.title()
        
        return df


def transform(df: pd.DataFrame, config: dict = None) -> pd.DataFrame:
    """
    Main transform function that applies all cleaning operations.
    
    Args:
        df: DataFrame to transform
        config: Optional configuration dictionary
        
    Returns:
        Cleaned and transformed DataFrame
    """
    logger.info("Starting data transformation")
    
    cleaner = BirthdayDataCleaner()
    
    # Apply cleaning operations
    df = cleaner.trim_whitespace(df)
    df = cleaner.handle_missing_values(df)
    df = cleaner.standardize_names(df)
    df = cleaner.parse_dob(df)
    df = cleaner.validate_email(df, drop_invalid=True)
    df = cleaner.remove_duplicates(df)
    
    # Drop rows where date parsing failed
    if 'dob_parsed' in df.columns:
        initial_count = len(df)
        df = df.dropna(subset=['dob_parsed'])
        removed_count = initial_count - len(df)
        if removed_count > 0:
            logger.warning(f"Dropped {removed_count} rows with unparseable dates")
    
    logger.info(f"Transformation complete. Final record count: {len(df)}")
    
    return df


if __name__ == "__main__":
    # Test the transform function
    sample_data = {
        'name': ['  john doe  ', 'JANE SMITH', 'Bob Johnson'],
        'email': ['john@example.com', 'invalid-email', 'bob@test.com'],
        'dob': ['1990-01-15', '1985/05/20', '1992-12-11']
    }
    df = pd.DataFrame(sample_data)
    print("Before transformation:")
    print(df)
    print("\nAfter transformation:")
    transformed_df = transform(df)
    print(transformed_df)
