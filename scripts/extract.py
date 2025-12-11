"""
Extract module for reading birthday data from various sources.
"""
import pandas as pd
import logging
from pathlib import Path
from typing import Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_from_csv(file_path: str) -> pd.DataFrame:
    """
    Extract data from a CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame containing the data
    """
    try:
        logger.info(f"Extracting data from CSV: {file_path}")
        df = pd.read_csv(file_path)
        logger.info(f"Successfully extracted {len(df)} records")
        return df
    except Exception as e:
        logger.error(f"Error extracting data from CSV: {str(e)}")
        raise


def extract_from_excel(file_path: str) -> pd.DataFrame:
    """
    Extract data from an Excel file.
    
    Args:
        file_path: Path to the Excel file
        
    Returns:
        DataFrame containing the data
    """
    try:
        logger.info(f"Extracting data from Excel: {file_path}")
        df = pd.read_excel(file_path)
        logger.info(f"Successfully extracted {len(df)} records")
        return df
    except Exception as e:
        logger.error(f"Error extracting data from Excel: {str(e)}")
        raise


def extract(file_path: Union[str, Path], file_type: str = None) -> pd.DataFrame:
    """
    Main extract function that determines file type and extracts data.
    
    Args:
        file_path: Path to the data file
        file_type: Type of file ('csv', 'excel'). If None, infers from extension
        
    Returns:
        DataFrame containing the data
    """
    file_path = Path(file_path)
    
    if file_type is None:
        # Infer file type from extension
        extension = file_path.suffix.lower()
        if extension == '.csv':
            file_type = 'csv'
        elif extension in ['.xlsx', '.xls']:
            file_type = 'excel'
        else:
            raise ValueError(f"Unsupported file extension: {extension}")
    
    if file_type == 'csv':
        return extract_from_csv(str(file_path))
    elif file_type == 'excel':
        return extract_from_excel(str(file_path))
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


if __name__ == "__main__":
    # Test the extract function
    test_file = "data/raw/birthdays.csv"
    try:
        df = extract(test_file)
        print(df.head())
    except Exception as e:
        print(f"Error: {e}")
