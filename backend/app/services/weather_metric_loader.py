# backend/app/services/weather_metric_loader.py

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
from ..models.weather_models_monthly import WeatherMonthly
from .weather_metric_processor import WeatherMetricProcessor
from .. import db

class WeatherMetricLoader:
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
            connection.execute(text('DROP TABLE IF EXISTS dbo.weather_matrics_monthly CASCADE;'))
            connection.commit()
        WeatherMonthly.__table__.create(self.engine)

    def load_data(self, csv_file: str) -> dict:
        session = self.Session()
        records_count = {}
        
        try:
            processor = WeatherMetricProcessor(csv_file)
            processed_data = processor.load_data()
            
            records = []
            for _, row in processed_data.iterrows():
                record = WeatherMonthly(
                    Year_value=row['Year'],
                    Month_value=row['Month'],
                    temp_mean=row['temp_mean'],
                    temp_max=row['temp_max'],
                    temp_min=row['temp_min'],
                    temp_std_dev=row['temp_std_dev'],
                    radiation_total=row['radiation_total'],
                    avg_peak_radiation=row['avg_peak_radiation'],
                    humidity_mean=row['humidity_mean'],
                    rain_total=row['rain_total'],
                    term_days=row['term_days'],
                    holiday_days=row['holiday_days'],
                    exam_days=row['exam_days'],
                    Mean_daily_Solar_energy=row['Mean_daily_Solar_energy'],
                    avg_wind_speed=row['avg_wind_speed'],
                    morning_temp_mean=row['morning_temp_mean'],
                    afternoon_temp_mean=row['afternoon_temp_mean'],
                    evening_temp_mean=row['evening_temp_mean'],
                    pressure_mean=row['pressure_mean'],
                    weighted_monthly_score=row['weighted_monthly_score']
                )
                records.append(record)
            
            session.bulk_save_objects(records)
            records_count['weather_monthly'] = len(records)
            session.commit()
            
            return records_count
            
        except Exception as e:
            session.rollback()
            raise Exception(f"Error loading Weather data: {str(e)}")
        finally:
            session.close()

    def verify_data(self) -> dict:
        session = self.Session()
        try:
            verification = {
                'weather_monthly': session.query(WeatherMonthly).count()
            }
            return verification
        finally:
            session.close()