# backend/app/services/stream_elec_loader.py

import pandas as pd
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker

from ..models.stream_elec_models import (
    RingMainsStream, LibrariesStream, CollegesStream, 
    ScienceStream, HealthScienceStream, HumanitiesStream,
    ObsPsychologyStream, TotalStreamDnElectricity,
    ItsServersStream, SchoolOfMedicineChChStream, CommerceStream
)
from .stream_elec_processor import StreamElecProcessor
from .. import db

class StreamElecLoader:
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
                DROP TABLE IF EXISTS dbo.ring_mains_stream CASCADE;
                DROP TABLE IF EXISTS dbo.libraries_stream CASCADE;
                DROP TABLE IF EXISTS dbo.colleges_stream CASCADE;
                DROP TABLE IF EXISTS dbo.science_stream CASCADE;
                DROP TABLE IF EXISTS dbo.health_science_stream CASCADE;
                DROP TABLE IF EXISTS dbo.humanities_stream CASCADE;
                DROP TABLE IF EXISTS dbo.obs_psychology_stream CASCADE;
                DROP TABLE IF EXISTS dbo.total_stream_dn_electricity CASCADE;
                DROP TABLE IF EXISTS dbo.its_servers_stream CASCADE;
                DROP TABLE IF EXISTS dbo.school_of_medicine_chch_stream CASCADE;
                DROP TABLE IF EXISTS dbo.commerce_stream CASCADE;
            '''))
            connection.commit()

            # Create all tables
            RingMainsStream.__table__.create(self.engine)
            LibrariesStream.__table__.create(self.engine)
            CollegesStream.__table__.create(self.engine)
            ScienceStream.__table__.create(self.engine)
            HealthScienceStream.__table__.create(self.engine)
            HumanitiesStream.__table__.create(self.engine)
            ObsPsychologyStream.__table__.create(self.engine)
            TotalStreamDnElectricity.__table__.create(self.engine)
            ItsServersStream.__table__.create(self.engine)
            SchoolOfMedicineChChStream.__table__.create(self.engine)
            CommerceStream.__table__.create(self.engine)

    def load_data(self, excel_file: str) -> dict:
        session = self.Session()
        records_count = {}

        try:
            processor = StreamElecProcessor(excel_file)
            processed_data = processor.load_all_data()

            table_models = {
                'ring_mains': RingMainsStream,
                'libraries': LibrariesStream,
                'colleges': CollegesStream,
                'science': ScienceStream,
                'health_science': HealthScienceStream,
                'humanities': HumanitiesStream,
                'obs_psychology': ObsPsychologyStream,
                'total_stream': TotalStreamDnElectricity,
                'its_servers': ItsServersStream,
                'school_of_medicine': SchoolOfMedicineChChStream,
                'commerce': CommerceStream
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
            raise Exception(f"Error loading Stream Electricity data: {str(e)}")
        finally:
            session.close()

    def verify_data(self) -> dict:
        session = self.Session()
        try:
            verification = {
                'ring_mains': session.query(RingMainsStream).count(),
                'libraries': session.query(LibrariesStream).count(),
                'colleges': session.query(CollegesStream).count(),
                'science': session.query(ScienceStream).count(),
                'health_science': session.query(HealthScienceStream).count(),
                'humanities': session.query(HumanitiesStream).count(),
                'obs_psychology': session.query(ObsPsychologyStream).count(),
                'total_stream': session.query(TotalStreamDnElectricity).count(),
                'its_servers': session.query(ItsServersStream).count(),
                'school_of_medicine': session.query(SchoolOfMedicineChChStream).count(),
                'commerce': session.query(CommerceStream).count()
            }
            return verification
        finally:
            session.close()
