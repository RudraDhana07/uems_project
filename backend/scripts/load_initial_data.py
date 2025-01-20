# backend/scripts/load_initial_data.py
import os
from dotenv import load_dotenv
from app.services.data_loader import DataLoader

def main():
    # Load environment variables
    load_dotenv()
    
    # Get database URL from environment variable
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    # Initialize data loader
    loader = DataLoader(db_url)
    
    # Create tables if they don't exist
    loader.create_tables()
    
    # Load water consumption data
    excel_file = os.path.join('data', '2024 campus meter readings.xlsx')
    try:
        records_count = loader.load_water_consumption_data(excel_file)
        print(f"Successfully loaded {records_count} records into the database")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()