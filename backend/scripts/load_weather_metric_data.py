# backend/scripts/load_weather_metric_data.py

import os
import sys
from pathlib import Path
import logging

current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.append(str(backend_dir))

from dotenv import load_dotenv
from app.services.weather_metric_loader import WeatherMetricLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    load_dotenv()
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")

    data_dir = backend_dir / 'data' / 'Weather'
    csv_file = data_dir / 'Load_weather_monthly.csv'

    if not csv_file.exists():
        raise FileNotFoundError(
            f"CSV file not found at {csv_file}. "
            f"Please place the file 'Load_weather_monthly.csv' "
            f"in the {data_dir} directory."
        )

    try:
        logger.info(f"Loading Weather data from: {csv_file}")
        loader = WeatherMetricLoader(db_url)
        
        logger.info("Creating schema...")
        loader.create_schema()
        
        logger.info("Creating tables...")
        loader.create_tables()
        
        logger.info("Loading data...")
        records = loader.load_data(str(csv_file))
        
        logger.info("\nRecords loaded:")
        for table_name, count in records.items():
            logger.info(f"{table_name}: {count} records")
            
        verification = loader.verify_data()
        logger.info("\nVerification Results:")
        for table_name, count in verification.items():
            logger.info(f"{table_name}: {count} records")
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

    logger.info("Data loading completed successfully")

if __name__ == "__main__":
    main()