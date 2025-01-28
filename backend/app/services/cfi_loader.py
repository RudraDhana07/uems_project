# backend/app/services/cfi_loader.py

import pandas as pd
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
from app.models.cfi_models import CenterForInnovation, CfiRoomTypes
from .cfi_processor import CfiProcessor
from .. import db

class CfiLoader:
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
                DROP TABLE IF EXISTS dbo.center_for_innovation CASCADE;
                DROP TABLE IF EXISTS dbo.cfi_room_types CASCADE;
            '''))
            connection.commit()

        CenterForInnovation.__table__.create(self.engine)
        CfiRoomTypes.__table__.create(self.engine)

    def load_data(self, excel_file: str) -> dict:
        session = self.Session()
        records_count = {}

        try:
            processor = CfiProcessor(excel_file)
            processed_data = processor.load_all_data()

            table_models = {
                'center_for_innovation': CenterForInnovation,
                'cfi_room_types': CfiRoomTypes
            }

            for table_name, data in processed_data.items():
                model_class = table_models[table_name]
                records = []

                # Filter out rows based on conditions
                if table_name == 'center_for_innovation':
                    data = data[data['location'].notna()]
                elif table_name == 'cfi_room_types':
                    data = data[data['room_number'].notna()]

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
            raise Exception(f"Error loading CFI data: {str(e)}")
        finally:
            session.close()

    def verify_data(self) -> dict:
        session = self.Session()
        try:
            verification = {
                'center_for_innovation': session.query(CenterForInnovation).count(),
                'cfi_room_types': session.query(CfiRoomTypes).count()
            }
            return verification
        finally:
            session.close()
