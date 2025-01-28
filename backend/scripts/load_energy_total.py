# backend/scripts/load_energy_total.py

import os
import sys
from pathlib import Path
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to Python path
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.append(str(backend_dir))

from dotenv import load_dotenv
from app.services.energy_total_loader import EnergyTotalLoader
from app.models.energy_total_models import EnergyTotalDashboard

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

    try:
        # Create database engine and session
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        logger.info("Creating schema and tables if they don't exist...")
        EnergyTotalDashboard.__table__.create(engine, checkfirst=True)
        
        logger.info("Loading energy total dashboard data...")
        loader = EnergyTotalLoader(session)
        records_loaded = loader.load_data()
        
        logger.info(f"Successfully loaded {records_loaded} records")
        
        # Verify data
        total_records = session.query(EnergyTotalDashboard).count()
        logger.info(f"Total records in database: {total_records}")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        session.close()

if __name__ == "__main__":
    main()
