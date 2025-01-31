# backend/scripts/load_weather_data.py

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from app.services.weather_loader import WeatherLoader
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



def main():
    try:
        # Load environment variables
        load_dotenv()
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            raise ValueError("DATABASE_URL environment variable not set")

        # Setup paths
        root_dir = Path(__file__).resolve().parent.parent
        weather_dir = root_dir / 'data' / 'Weather'
        calendar_dir = root_dir / 'data' / 'calendar'

        # Verify required files exist
        required_files = {
            'merged_data': weather_dir / 'merged_weather_data.csv',
            'weights': weather_dir / 'Weather_Weights.xlsx',
            'calendar': calendar_dir / 'Otago_Calendar.xlsx',
            'solar_energy': weather_dir / 'Mean_solar_Energy.csv'
        }

        for name, path in required_files.items():
            if not path.exists():
                raise FileNotFoundError(f"{name} file not found at: {path}")

        # Initialize loader
        logger.info("Initializing weather data loader...")
        loader = WeatherLoader(db_url)

        # Create schema and tables
        logger.info("Creating database schema...")
        loader.create_schema()

        logger.info("Creating tables...")
        loader.create_tables()

        # Load reference data first
        logger.info("Loading weather weights...")
        weights_count = loader.load_weather_weights(required_files['weights'])
        logger.info(f"Loaded {weights_count} weather weight records")

        logger.info("Loading academic calendar...")
        calendar_count = loader.load_academic_calendar(required_files['calendar'])
        logger.info(f"Loaded {calendar_count} academic calendar records")

        solar_count = loader.load_solar_energy(required_files['solar_energy'])
        logger.info(f"Loaded {solar_count} solar energy records")

        loader.verify_solar_energy_data()

        # Load and process weather data
        logger.info("Processing weather data...")
        records = loader.load_weather_data(required_files['merged_data'])
        logger.info(f"Processed {records['daily']} daily records")
        logger.info(f"Processed {records['monthly']} monthly records")

        # Verify loaded data
        logger.info("Verifying loaded data...")
        verification = loader.verify_data()
        
        logger.info("\nData Verification Results:")
        logger.info(f"Daily Records: {verification['daily_records']}")
        logger.info(f"Monthly Records: {verification['monthly_records']}")
        logger.info(f"Weather Weights: {verification['weather_weights']}")
        logger.info(f"Academic Calendar: {verification['academic_calendar']}")
        
        if 'daily_date_range' in verification:
            logger.info(f"Daily Data Range: {verification['daily_date_range']['start']} "
                       f"to {verification['daily_date_range']['end']}")
        
        if 'monthly_date_range' in verification:
            logger.info(f"Monthly Data Range: {verification['monthly_date_range']['start']} "
                       f"to {verification['monthly_date_range']['end']}")

    except Exception as e:
        logger.error(f"Error during weather data loading: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()