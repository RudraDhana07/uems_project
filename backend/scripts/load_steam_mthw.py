#!/usr/bin/env python3
# backend/scripts/load_steam_mthw.py

import os
import sys
from pathlib import Path

# Add the parent directory to Python path
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.append(str(backend_dir))

from dotenv import load_dotenv
from app.services.steam_mthw_loader import SteamMTHWLoader

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
        print(f"Loading Steam and MTHW data from: {excel_file}")
        
        # Initialize loader
        loader = SteamMTHWLoader(db_url)
        
        # Create schema and tables
        print("Creating schema...")
        loader.create_schema()
        
        print("Recreating tables...")
        loader.recreate_tables()
        
        # Load data
        print("Loading data...")
        records_loaded = loader.load_data(str(excel_file))
        print(f"Successfully loaded {records_loaded} records")
        
        # Verify data
        verification = loader.verify_data()
        print(f"\nTotal records in database: {verification['total_records']}")
        print(f"Date range: {verification['date_range']['start']} to {verification['date_range']['end']}")
                
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()