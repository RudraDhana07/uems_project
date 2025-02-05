# backend/app/services/auckland_calculated_water_loader.py

import pandas as pd
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
from ..models.auckland_water import AucklandWaterCalculatedConsumption
from .auckland_calculated_water_processor import AucklandCalculatedWaterProcessor
from .. import db

class AucklandCalculatedWaterLoader:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData(schema='dbo')

    def create_schema(self):
        """Create database schema if it doesn't exist"""
        with self.engine.begin() as connection:
            connection.execute(text('CREATE SCHEMA IF NOT EXISTS dbo;'))

    def create_tables(self):
        """Drop and recreate only the calculated water consumption table"""
        with self.engine.begin() as connection:
            connection.execute(text('''
                DROP SEQUENCE IF EXISTS dbo.auckland_water_calculated_consumption_id_seq CASCADE;
                DROP TABLE IF EXISTS dbo.auckland_water_calculated_consumption CASCADE;
            '''))
            AucklandWaterCalculatedConsumption.__table__.create(self.engine)

    def load_data(self, excel_file: str) -> int:
        """Load calculated water consumption data from Excel"""
        session = self.Session()
        try:
            calc_processor = AucklandCalculatedWaterProcessor(excel_file)
            calc_data = calc_processor.load_data()
            calc_records = []

            for _, row in calc_data.iterrows():
                record = AucklandWaterCalculatedConsumption(
                    object_name=row['object_name'],
                    object_description=row['object_description'],
                    meter_location=row['meter_location']
                )
                
                for col in calc_data.columns:
                    if col not in ['object_name', 'object_description', 'meter_location']:
                        value = row[col]
                        if pd.isna(value):
                            value = None
                        setattr(record, col, value)
                calc_records.append(record)

            session.bulk_save_objects(calc_records)
            session.commit()
            return len(calc_records)

        except Exception as e:
            session.rollback()
            raise Exception(f"Error loading Auckland Calculated Water data: {str(e)}")
        finally:
            session.close()

    def verify_data(self) -> dict:
        """Verify loaded data"""
        session = self.Session()
        try:
            calc_records = session.query(AucklandWaterCalculatedConsumption).count()
            return {'calculated_records': calc_records}
        finally:
            session.close()
