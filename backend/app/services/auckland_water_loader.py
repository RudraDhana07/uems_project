# backend/app/services/auckland_water_loader.py

import pandas as pd
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
from ..models.auckland_water import AucklandWaterConsumption
from .auckland_water_processor import AucklandWaterProcessor
from .. import db

class AucklandWaterLoader:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData(schema='dbo')
        
    def create_schema(self):
        """Create database schema if it doesn't exist"""
        with self.engine.connect() as connection:
            connection.execute(text('CREATE SCHEMA IF NOT EXISTS dbo;'))
            connection.commit()
            
    def create_tables(self):
        """Drop and recreate only the water consumption table"""
        with self.engine.connect() as connection:
            # Drop only this specific table
            connection.execute(text('''
                DROP TABLE IF EXISTS dbo.auckland_water_consumption CASCADE;
            '''))
            connection.commit()
        
        # Create table
        AucklandWaterConsumption.__table__.create(self.engine)
            
    def load_data(self, excel_file: str) -> int:
        """Load water consumption data from Excel"""
        session = self.Session()
        try:
            water_processor = AucklandWaterProcessor(excel_file)
            water_data = water_processor.load_data()
            
            water_records = []
            for _, row in water_data.iterrows():
                record = AucklandWaterConsumption(
                    object_name=row['object_name'],
                    object_description=row['object_description'],
                    reading_description=row['reading_description']
                )
                
                # Add each month's reading
                for col in water_data.columns:
                    if col not in ['object_name', 'object_description', 'reading_description']:
                        value = row[col]
                        if pd.isna(value):
                            value = None
                        setattr(record, col, value)
                
                water_records.append(record)
            
            session.bulk_save_objects(water_records)
            session.commit()
            
            return len(water_records)
            
        except Exception as e:
            session.rollback()
            raise Exception(f"Error loading Auckland Water data: {str(e)}")
        
        finally:
            session.close()
            
    def verify_data(self) -> dict:
        """Verify loaded data"""
        session = self.Session()
        try:
            water_records = session.query(AucklandWaterConsumption).count()
            return {
                'water_records': water_records
            }
        finally:
            session.close()

