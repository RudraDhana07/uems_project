# backend/app/services/janitza_loader.py

import pandas as pd
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
from ..models.janitza_models import (
    JanitzaMedData, JanitzaFreezerRoom, JanitzaUOD4F6,
    JanitzaUOF8X, JanitzaManualMeters, JanitzaCalculatedConsumption
)
from .janitza_processor import JanitzaProcessor
from .. import db

class JanitzaLoader:
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
        """Drop and recreate all Janitza tables"""
        with self.engine.connect() as connection:
            # Drop existing tables
            connection.execute(text('''
                DROP TABLE IF EXISTS dbo.janitza_med_data CASCADE;
                DROP TABLE IF EXISTS dbo.janitza_freezer_room CASCADE;
                DROP TABLE IF EXISTS dbo.janitza_uo_d4f6 CASCADE;
                DROP TABLE IF EXISTS dbo.janitza_uo_f8x CASCADE;
                DROP TABLE IF EXISTS dbo.janitza_manual_meters CASCADE;
                DROP TABLE IF EXISTS dbo.janitza_calculated_consumption CASCADE;
            '''))
            connection.commit()
            
        # Create tables
        JanitzaMedData.__table__.create(self.engine)
        JanitzaFreezerRoom.__table__.create(self.engine)
        JanitzaUOD4F6.__table__.create(self.engine)
        JanitzaUOF8X.__table__.create(self.engine)
        JanitzaManualMeters.__table__.create(self.engine)
        JanitzaCalculatedConsumption.__table__.create(self.engine)
    
    def load_data(self, excel_file: str) -> dict:
        """Load all Janitza data from Excel"""
        session = self.Session()
        records_count = {}
        
        try:
            processor = JanitzaProcessor(excel_file)
            processed_data = processor.load_all_data()
            
            # Map table names to model classes
            table_models = {
                'med_data': JanitzaMedData,
                'freezer_room': JanitzaFreezerRoom,
                'uo_d4f6': JanitzaUOD4F6,
                'uo_f8x': JanitzaUOF8X,
                'manual_meters': JanitzaManualMeters,
                'calculated_consumption': JanitzaCalculatedConsumption
            }
            
            # Process each table
            for table_name, data in processed_data.items():
                model_class = table_models[table_name]
                records = []
                
                for _, row in data.iterrows():
                    record = model_class(
                        meter_location=row['meter_location']
                    )
                    
                    # Set values for each month column
                    for col in data.columns:
                        if col != 'meter_location':
                            value = row[col]
                            if pd.isna(value):
                                value = None
                            setattr(record, col, value)
                    
                    records.append(record)
                
                session.bulk_save_objects(records)
                records_count[table_name] = len(records)
            
            session.commit()
            return records_count
            
        except Exception as e:
            session.rollback()
            raise Exception(f"Error loading Janitza data: {str(e)}")
        finally:
            session.close()
    
    def verify_data(self) -> dict:
        """Verify loaded data for all tables"""
        session = self.Session()
        try:
            verification = {
                'med_data': session.query(JanitzaMedData).count(),
                'freezer_room': session.query(JanitzaFreezerRoom).count(),
                'uo_d4f6': session.query(JanitzaUOD4F6).count(),
                'uo_f8x': session.query(JanitzaUOF8X).count(),
                'manual_meters': session.query(JanitzaManualMeters).count(),
                'calculated_consumption': session.query(JanitzaCalculatedConsumption).count()
            }
            return verification
        finally:
            session.close()
