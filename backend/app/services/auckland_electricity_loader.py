# backend/app/services/auckland_electricity_loader.py

import pandas as pd
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
from ..models.auckland_electricity import AucklandElectricityCalculatedConsumption
from .auckland_electricity_processor import AucklandElectricityProcessor
from .. import db

class AucklandElectricityLoader:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData(schema='dbo')
        
    def create_schema(self):
        """Create database schema if it doesn't exist"""
        with self.engine.begin() as connection:
            connection.execute(text('CREATE SCHEMA IF NOT EXISTS dbo;'))
            
    def recreate_tables(self):
        """Drop and recreate only the electricity consumption table"""
        with self.engine.begin() as connection:
            # Drop only this specific table
            connection.execute(text('''
                DROP TABLE IF EXISTS dbo.auckland_electricity_calculated_consumption CASCADE;
            '''))
        
        # Create only this table
        AucklandElectricityCalculatedConsumption.__table__.create(self.engine)
            
    def load_data(self, excel_file: str) -> int:
        """Load data from Excel to database"""
        session = self.Session()
        try:
            processor = AucklandElectricityProcessor(excel_file)
            raw_data = processor.load_data()
            
            records = []
            for _, row in raw_data.iterrows():
                record = AucklandElectricityCalculatedConsumption(
                    object_name=row['object_name'],
                    object_description=row['object_description'],
                    meter_location=row['meter_location']
                )
                
                # Add each month's reading
                for col in raw_data.columns:
                    if col not in ['object_name', 'object_description', 'meter_location']:
                        value = row[col]
                        if pd.isna(value):
                            value = None
                        setattr(record, col, value)
                
                records.append(record)
            
            session.bulk_save_objects(records)
            session.commit()
            
            return len(records)
            
        except Exception as e:
            session.rollback()
            raise Exception(f"Error loading Auckland Electricity data: {str(e)}")
        
        finally:
            session.close()
            
    def verify_data(self) -> dict:
        """Verify loaded data"""
        session = self.Session()
        try:
            total_records = session.query(AucklandElectricityCalculatedConsumption).count()
            return {'total_records': total_records}
        finally:
            session.close()