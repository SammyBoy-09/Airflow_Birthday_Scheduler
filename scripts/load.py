"""
Load module for saving processed birthday data.
"""
import pandas as pd
import logging
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_to_csv(df: pd.DataFrame, file_path: str) -> None:
    """
    Save DataFrame to CSV file.
    
    Args:
        df: DataFrame to save
        file_path: Path to save the CSV file
    """
    try:
        logger.info(f"Saving data to CSV: {file_path}")
        
        # Create directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(file_path, index=False)
        logger.info(f"Successfully saved {len(df)} records to {file_path}")
    except Exception as e:
        logger.error(f"Error saving to CSV: {str(e)}")
        raise


def save_to_excel(df: pd.DataFrame, file_path: str) -> None:
    """
    Save DataFrame to Excel file.
    
    Args:
        df: DataFrame to save
        file_path: Path to save the Excel file
    """
    try:
        logger.info(f"Saving data to Excel: {file_path}")
        
        # Create directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        df.to_excel(file_path, index=False, engine='openpyxl')
        logger.info(f"Successfully saved {len(df)} records to {file_path}")
    except Exception as e:
        logger.error(f"Error saving to Excel: {str(e)}")
        raise


def load(df: pd.DataFrame, 
         csv_path: Optional[str] = None,
         excel_path: Optional[str] = None) -> None:
    """
    Main load function that saves data to specified formats.
    
    Args:
        df: DataFrame to save
        csv_path: Optional path to save CSV file
        excel_path: Optional path to save Excel file
    """
    logger.info("Starting data loading")
    
    if csv_path:
        save_to_csv(df, csv_path)
    
    if excel_path:
        save_to_excel(df, excel_path)
    
    if not csv_path and not excel_path:
        logger.warning("No output paths specified. Data not saved.")
    
    logger.info("Data loading complete")


if __name__ == "__main__":
    # Test the load function
    sample_data = {
        'name': ['John Doe', 'Jane Smith'],
        'email': ['john@example.com', 'jane@example.com'],
        'dob': ['1990-01-15', '1985-05-20']
    }
    df = pd.DataFrame(sample_data)
    
    load(df, 
         csv_path="data/processed/test_output.csv",
         excel_path="data/processed/test_output.xlsx")
