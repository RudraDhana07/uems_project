# backend/app/services/mthw_loader.py

import pandas as pd
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
from app.models.mthw_models import (
    MTHWMeterReading,
    MTHWConsumptionReading
)
from .. import db
from .mthw_processor import MTHWProcessor

class MTHWLoader:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData(schema='dbo')

    def create_schema(self):
        with self.engine.connect() as connection:
            connection.execute(text('CREATE SCHEMA IF NOT EXISTS dbo;'))
            connection.commit()

    def create_tables(self):
        with self.engine.connect() as connection:
            connection.execute(text('''
                DROP TABLE IF EXISTS dbo.mthw_meter_reading CASCADE;
                DROP TABLE IF EXISTS dbo.mthw_consumption_reading CASCADE;
            '''))
            connection.commit()

        MTHWMeterReading.__table__.create(self.engine)
        MTHWConsumptionReading.__table__.create(self.engine)

    def load_data(self, excel_file: str) -> dict:
        session = self.Session()
        records_count = {}

        try:
            processor = MTHWProcessor(excel_file)
            processed_data = processor.load_all_data()

            table_models = {
                'meter_reading': MTHWMeterReading,
                'consumption_reading': MTHWConsumptionReading
            }

            for table_name, data in processed_data.items():
                model_class = table_models[table_name]
                records = []

                for _, row in data.iterrows():
                    record = model_class()
                    for col in data.columns:
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
            raise Exception(f"Error loading MTHW data: {str(e)}")
        finally:
            session.close()

    def verify_data(self) -> dict:
        session = self.Session()
        try:
            verification = {
                'meter_reading': session.query(MTHWMeterReading).count(),
                'consumption_reading': session.query(MTHWConsumptionReading).count()
            }
            return verification
        finally:
            session.close()
