# backend/app/services/steam_mthw_loader.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from ..models.steam_mthw import SteamMTHWReading
from .steam_mthw_processor import SteamMTHWProcessor
import pandas as pd

class SteamMTHWLoader:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        
    def create_schema(self):
        """Create database schema if it doesn't exist"""
        with self.engine.connect() as connection:
            connection.execute(text('CREATE SCHEMA IF NOT EXISTS dbo;'))
            connection.commit()
            
    def recreate_tables(self):
        """Drop and recreate only the steam_mthw_readings table"""
        with self.engine.connect() as connection:
            # Drop only this specific table
            connection.execute(text('''
                DROP TABLE IF EXISTS dbo.steam_mthw_readings CASCADE;
            '''))
            connection.commit()
        
        # Create only this table
        SteamMTHWReading.__table__.create(self.engine)
            
    def load_data(self, excel_file: str) -> int:
        """Load data from Excel to database"""
        session = self.Session()
        try:
            processor = SteamMTHWProcessor(excel_file)
            raw_data = processor.load_data()
            
            records = []
            for _, row in raw_data.iterrows():
                record = SteamMTHWReading(
                    month=row['month'],
                    year=row['year'],
                    mthw_consumption_kwh=row['mthw_consumption_kwh'],
                    castle_192_reading_kwh=row['castle_192_reading_kwh'],
                    castle_192_consumption_kwh=row['castle_192_consumption_kwh'],
                    med_school_a_reading_kg=row['med_school_a_reading_kg'],
                    med_school_a_reading_kwh=row['med_school_a_reading_kwh'],
                    med_school_a_consumption_kg=row['med_school_a_consumption_kg'],
                    med_school_a_consumption_kwh=row['med_school_a_consumption_kwh'],
                    med_school_b_reading_kg=row['med_school_b_reading_kg'],
                    med_school_b_reading_kwh=row['med_school_b_reading_kwh'],
                    med_school_b_consumption_kg=row['med_school_b_consumption_kg'],
                    med_school_b_consumption_kwh=row['med_school_b_consumption_kwh'],
                    med_school_consumption_kg=row['med_school_consumption_kg'],
                    med_school_consumption_kwh=row['med_school_consumption_kwh'],
                    cumberland_d401_dining_reading_kg=row['cumberland_d401_dining_reading_kg'],
                    cumberland_d404_castle_reading_kg=row['cumberland_d404_castle_reading_kg'],
                    cumberland_d401_d404_consumption_kg=row['cumberland_d401_d404_consumption_kg'],
                    cumberland_d401_d404_consumption_kwh=row['cumberland_d401_d404_consumption_kwh'],
                    total_steam_consumption_kwh=row['total_steam_consumption_kwh']
                )
                records.append(record)
            
            session.bulk_save_objects(records)
            session.commit()
            
            return len(records)
            
        except Exception as e:
            session.rollback()
            raise Exception(f"Error loading Steam and MTHW data: {str(e)}")
        
        finally:
            session.close()
            
    def verify_data(self) -> dict:
        """Verify loaded data"""
        session = self.Session()
        try:
            result = {}
            
            # Get total number of records
            result['total_records'] = session.query(SteamMTHWReading).count()
            
            # Get date range
            date_range = session.query(
                text("MIN(month || ' ' || year)"), 
                text("MAX(month || ' ' || year)")
            ).select_from(SteamMTHWReading).first()
            
            result['date_range'] = {
                'start': date_range[0] if date_range[0] else None,
                'end': date_range[1] if date_range[1] else None
            }
            
            return result
            
        finally:
            session.close()