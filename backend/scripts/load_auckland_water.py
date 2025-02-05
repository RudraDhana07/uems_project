# backend/scripts/load_auckland_water.py

import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup path for local execution
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent

import sys
sys.path.append(str(backend_dir.parent))

def load_auckland_water(excel_filename='2024 campus meter readings.xlsx'):
    """
    Load Auckland water consumption data from Excel file
    
    Args:
        excel_filename (str): Name of the Excel file to process
        
    Returns:
        int: Number of records loaded
    """
    try:
        # Get database URL
        from dotenv import load_dotenv
        load_dotenv()
        
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            raise ValueError("DATABASE_URL environment variable not set")

        # Setup data directory path
        data_dir = backend_dir / 'data'
        excel_file = data_dir / excel_filename
        
        if not excel_file.exists():
            raise FileNotFoundError(f"Excel file not found at {excel_file}")

        # Import after path setup
        from backend.app.services.auckland_water_loader import AucklandWaterLoader
        
        logger.info(f"Loading water consumption data from: {excel_file}")
        
        loader = AucklandWaterLoader(db_url)
        
        logger.info("Creating schema...")
        loader.create_schema()
        
        logger.info("Creating tables...")
        loader.create_tables()
        
        logger.info("Loading data...")
        records_loaded = loader.load_data(str(excel_file))
        
        logger.info(f"Successfully loaded {records_loaded} records")
        
        verification = loader.verify_data()
        logger.info(f"Total water consumption records: {verification.get('water_records', 0)}")
        
        return records_loaded

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        records_loaded = load_auckland_water()
        print(f"Script completed successfully. Loaded {records_loaded} records.")
    except Exception as e:
        print(f"Error executing script: {e}")
        sys.exit(1)
