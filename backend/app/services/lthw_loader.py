# backend/app/services/lthw_loader.py

import pandas as pd
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
from ..models.lthw_models import (
    LTHWAutomatedMeter, LTHWManualMeter, LTHWConsumption
)
from .lthw_processor import LTHWProcessor
from .. import db

class LTHWLoader:
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
                DROP TABLE IF EXISTS dbo.lthw_automated_meter CASCADE;
                DROP TABLE IF EXISTS dbo.lthw_manual_meter CASCADE;
                DROP TABLE IF EXISTS dbo.lthw_consumption CASCADE;
            '''))
            connection.commit()

            LTHWAutomatedMeter.__table__.create(self.engine)
            LTHWManualMeter.__table__.create(self.engine)
            LTHWConsumption.__table__.create(self.engine)

    def load_data(self, excel_file: str) -> dict:
        session = self.Session()
        records_count = {}

        try:
            processor = LTHWProcessor(excel_file)
            processed_data = processor.load_all_data()

            table_models = {
                'automated_meter': LTHWAutomatedMeter,
                'manual_meter': LTHWManualMeter,
                'consumption': LTHWConsumption
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
            raise Exception(f"Error loading LTHW data: {str(e)}")
        finally:
            session.close()

    def verify_data(self) -> dict:
        session = self.Session()
        try:
            verification = {
                'automated_meter': session.query(LTHWAutomatedMeter).count(),
                'manual_meter': session.query(LTHWManualMeter).count(),
                'consumption': session.query(LTHWConsumption).count()
            }
            return verification
        finally:
            session.close()
