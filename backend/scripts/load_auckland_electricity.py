# backend/scripts/load_auckland_electricity.py

import os
import sys
from pathlib import Path
import logging

# Add the parent directory to Python path
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.append(str(backend_dir))

from dotenv import load_dotenv
from app.services.auckland_electricity_loader import AucklandElectricityLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_auckland_electricity(excel_filename='2024 campus meter readings.xlsx'):
    """
    Load Auckland electricity data from Excel file
    Args:
        excel_filename (str): Name of the Excel file to process
    Returns:
        int: Number of records loaded
    """
    # Load environment variables
    load_dotenv()
    
    # Get database URL
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")
    

    excel_filename = os.getenv('DATA_FILE')
    
    print(f"Loading data from file: {excel_filename}")
    
    # Setup data directory path
    data_dir = backend_dir / 'data'
    excel_file = data_dir / excel_filename
    
    # Verify file exists
    if not excel_file.exists():
        raise FileNotFoundError(
            f"Excel file not found at {excel_file}. "
            f"Please place the file '{excel_filename}' "
            f"in the {data_dir} directory."
        )
    
    try:
        logger.info(f"Loading electricity consumption data from: {excel_file}")
        
        # Initialize loader
        loader = AucklandElectricityLoader(db_url)
        
        # Create schema and tables
        logger.info("Creating schema...")
        loader.create_schema()
        
        logger.info("Recreating tables...")
        loader.recreate_tables()
        
        # Load data
        logger.info("Loading data...")
        records_loaded = loader.load_data(str(excel_file))
        logger.info(f"Successfully loaded {records_loaded} records")
        
        # Verify data
        verification = loader.verify_data()
        logger.info(f"Total records in database: {verification['total_records']}")
        
        return records_loaded
                
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise

# For local execution
if __name__ == "__main__":
    try:
        records_loaded = load_auckland_electricity()
        print(f"Script completed successfully. Loaded {records_loaded} records.")
    except Exception as e:
        print(f"Error executing script: {e}")
        sys.exit(1)
