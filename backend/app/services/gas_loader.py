# backend/app/services/gas_loader.py

import pandas as pd
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
from ..models.gas_models import (
    GasAutomatedMeter, GasManualMeter, GasConsumption
)
from .gas_processor import GasProcessor
from .. import db

class GasLoader:
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
                DROP TABLE IF EXISTS dbo.gas_automated_meter CASCADE;
                DROP TABLE IF EXISTS dbo.gas_manual_meter CASCADE;
                DROP TABLE IF EXISTS dbo.gas_consumption CASCADE;
            '''))
            connection.commit()

            GasAutomatedMeter.__table__.create(self.engine)
            GasManualMeter.__table__.create(self.engine)
            GasConsumption.__table__.create(self.engine)

    def load_data(self, excel_file: str) -> dict:
        session = self.Session()
        records_count = {}

        try:
            processor = GasProcessor(excel_file)
            processed_data = processor.load_all_data()

            table_models = {
                'automated_meter': GasAutomatedMeter,
                'manual_meter': GasManualMeter,
                'consumption': GasConsumption
            }

            for table_name, data in processed_data.items():
                model_class = table_models[table_name]
                records = []

                for _, row in data.iterrows():
                    record = model_class()
                    
                    # Set values for all columns
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
            raise Exception(f"Error loading Gas data: {str(e)}")
        finally:
            session.close()

    def verify_data(self) -> dict:
        session = self.Session()
        try:
            verification = {
                'automated_meter': session.query(GasAutomatedMeter).count(),
                'manual_meter': session.query(GasManualMeter).count(),
                'consumption': session.query(GasConsumption).count()
            }
            return verification
        finally:
            session.close()
