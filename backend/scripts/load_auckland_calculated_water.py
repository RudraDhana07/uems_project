# backend/scripts/load_auckland_calculated_water.py

import os
import sys
from pathlib import Path
import logging

# Add the parent directory to Python path
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.append(str(backend_dir))

from dotenv import load_dotenv
from app.services.auckland_calculated_water_loader import AucklandCalculatedWaterLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Load environment variables
    load_dotenv()
    
    # Get database URL
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    # Setup data directory path
    data_dir = backend_dir / 'data'
    excel_file = data_dir / '2024 campus meter readings.xlsx'
    
    # Verify file exists
    if not excel_file.exists():
        raise FileNotFoundError(
            f"Excel file not found at {excel_file}. "
            f"Please place the file '2024 campus meter readings.xlsx' "
            f"in the {data_dir} directory."
        )
    
    try:
        logger.info(f"Loading calculated water consumption data from: {excel_file}")
        
        # Initialize loader
        loader = AucklandCalculatedWaterLoader(db_url)
        
        # Create schema and tables
        logger.info("Creating schema...")
        loader.create_schema()
        
        logger.info("Creating tables...")
        loader.create_tables()
        
        # Load data
        logger.info("Loading data...")
        records_loaded = loader.load_data(str(excel_file))
        logger.info(f"Successfully loaded {records_loaded} records")
        
        # Verify data
        verification = loader.verify_data()
        logger.info("\nVerification Results:")
        logger.info(f"Calculated Water Records: {verification.get('calculated_records', 0)}")
                
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)
    
    logger.info("Data loading completed successfully")

if __name__ == "__main__":
    main()