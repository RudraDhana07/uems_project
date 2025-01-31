# backend/app/services/weather_loader.py

import pandas as pd
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
from ..models.weather_models import (
    WeatherDaily,
    WeatherMonthly,
    WeatherWeights,
    AcademicCalendar
)
from .weather_processor import WeatherProcessor
from .weather_preprocessor import WeatherDataPreprocessor
from .. import db
import logging

logger = logging.getLogger(__name__)

class WeatherLoader:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData(schema='dbo')
        self.academic_calendar_df = None
        self.weather_weights_df = None
        self.processor = None
        self.solar_energy_df = None

    def create_schema(self):
        """Create database schema if it doesn't exist"""
        with self.engine.connect() as connection:
            connection.execute(text('CREATE SCHEMA IF NOT EXISTS dbo;'))
            connection.commit()

    def create_tables(self):
        """Drop and recreate all weather-related tables"""
        with self.engine.connect() as connection:
            # Drop existing tables in correct order
            connection.execute(text('''
                DROP TABLE IF EXISTS dbo.weather_daily CASCADE;
                DROP TABLE IF EXISTS dbo.weather_monthly CASCADE;
                DROP TABLE IF EXISTS dbo.weather_weights CASCADE;
                DROP TABLE IF EXISTS dbo.academic_calendar CASCADE;
            '''))
            connection.commit()

            # Create tables using models
            WeatherDaily.__table__.create(self.engine)
            WeatherMonthly.__table__.create(self.engine)
            WeatherWeights.__table__.create(self.engine)
            AcademicCalendar.__table__.create(self.engine)

    # backend/app/services/weather_loader.py

    def load_weather_weights(self, file_path: str) -> int:
        """Load weather weights from Excel file"""
        session = self.Session()
        try:
            logger.info("Loading weather weights from Excel...")
            self.weather_weights_df = pd.read_excel(file_path)
            
            # Create mapping for column names to model fields
            column_mapping = {
                'Season': 'season',
                'Temp_Weight': 'temp_weight',
                'radiation_Weight': 'radiation_weight',
                'humidity_weight': 'humidity_weight',
                'wind_Weight': 'wind_weight',
                'term_multiplier': 'term_multiplier',
                'summer_break_multiplier': 'summer_break_multiplier',
                'mid_sum_multiplier': 'mid_sum_multiplier',
                'exam_multiplier': 'exam_multiplier',
                'Public_multiplier': 'public_multiplier',
                'Sunday_multiplier': 'sunday_multiplier'
            }
            
            records = []
            for _, row in self.weather_weights_df.iterrows():
                record = WeatherWeights()
                for excel_col, model_field in column_mapping.items():
                    if excel_col in row.index and pd.notna(row[excel_col]):
                        setattr(record, model_field, row[excel_col])
                records.append(record)

            session.bulk_save_objects(records)
            session.commit()
            return len(records)

        except Exception as e:
            session.rollback()
            raise Exception(f"Error loading weather weights: {str(e)}")
        finally:
            session.close()

    def load_academic_calendar(self, file_path: str) -> int:
        """Load academic calendar from Excel file"""
        session = self.Session()
        try:
            logger.info("Loading academic calendar from Excel...")
            self.academic_calendar_df = pd.read_excel(file_path)
            self.academic_calendar_df['date_id'] = pd.to_datetime(self.academic_calendar_df['date_id'])
            records = []

            for _, row in self.academic_calendar_df.iterrows():
                record = AcademicCalendar()
                for column in row.index:
                    if pd.notna(row[column]):
                        setattr(record, column.lower(), row[column])
                records.append(record)

            session.bulk_save_objects(records)
            session.commit()
            return len(records)

        except Exception as e:
            session.rollback()
            raise Exception(f"Error loading academic calendar: {str(e)}")
        finally:
            session.close()

    def load_weather_data(self, merged_file_path: str) -> dict:
        """Load and process weather data"""
        session = self.Session()
        records_count = {}

        try:
            logger.info("Processing weather data...")
            
            # Initialize preprocessor and process data
            preprocessor = WeatherDataPreprocessor()
            processed_df = preprocessor.preprocess_data(merged_file_path)
            
            # Validate processed data
            validation_results = preprocessor.validate_data(processed_df)
            logger.info(f"Data validation completed")
            
            # Initialize processor with required dataframes
            self.processor = WeatherProcessor(
                self.academic_calendar_df,
                self.weather_weights_df,
                self.solar_energy_df
            )

            # Process daily data
            daily_data = self.processor.process_daily(processed_df)
            daily_records = []
            
            for date_id, row in daily_data.iterrows():
                record = WeatherDaily(date_id=date_id)
                for column, value in row.items():
                    if pd.notna(value):
                        setattr(record, column, value)
                daily_records.append(record)

            # Process monthly data
            monthly_data = self.processor.process_monthly(daily_data)
            monthly_records = []
            
            for date_id, row in monthly_data.iterrows():
                record = WeatherMonthly(month_id=date_id)
                for column, value in row.items():
                    if pd.notna(value):
                        setattr(record, column, value)
                monthly_records.append(record)

            # Save records
            session.bulk_save_objects(daily_records)
            session.bulk_save_objects(monthly_records)
            session.commit()

            # Prepare return data
            records_count = {
                'daily': len(daily_records),
                'monthly': len(monthly_records),
                'validation': validation_results
            }

            # Log loading summary
            logger.info(f"Successfully loaded {len(daily_records)} daily records")
            logger.info(f"Successfully loaded {len(monthly_records)} monthly records")
            logger.info(f"Data completeness: {validation_results['data_quality']['completeness']['percentage']:.2f}%")

            return records_count

        except Exception as e:
            session.rollback()
            raise Exception(f"Error loading weather data: {str(e)}")
        finally:
            session.close()


    def load_solar_energy(self, file_path):
        """Load solar energy data from CSV"""
        try:
            logger.info(f"Loading solar energy data from: {file_path}")
            self.solar_energy_df = pd.read_csv(file_path)
            logger.info(f"Initial solar energy data shape: {self.solar_energy_df.shape}")
            logger.debug(f"Columns in solar energy file: {self.solar_energy_df.columns.tolist()}")
            
            # Convert to datetime
            self.solar_energy_df['Date'] = pd.to_datetime(
                self.solar_energy_df[['Year', 'Month']].assign(DAY=1)
            )
            logger.info("Date conversion completed")
            logger.debug(f"Sample data:\n{self.solar_energy_df.head()}")
            
            return len(self.solar_energy_df)
        except Exception as e:
            logger.error(f"Error loading solar energy data: {str(e)}")
            logger.error(f"File path: {file_path}")
            raise

    def verify_data(self) -> dict:
        """Verify loaded data counts"""
        session = self.Session()
        try:
            verification = {
                'daily_records': session.query(WeatherDaily).count(),
                'monthly_records': session.query(WeatherMonthly).count(),
                'weather_weights': session.query(WeatherWeights).count(),
                'academic_calendar': session.query(AcademicCalendar).count()
            }

            # Additional verification for date ranges
            if verification['daily_records'] > 0:
                daily_range = session.query(
                    db.func.min(WeatherDaily.date_id),
                    db.func.max(WeatherDaily.date_id)
                ).first()
                verification['daily_date_range'] = {
                    'start': daily_range[0].strftime('%Y-%m-%d'),
                    'end': daily_range[1].strftime('%Y-%m-%d')
                }

            if verification['monthly_records'] > 0:
                monthly_range = session.query(
                    db.func.min(WeatherMonthly.month_id),
                    db.func.max(WeatherMonthly.month_id)
                ).first()
                verification['monthly_date_range'] = {
                    'start': monthly_range[0].strftime('%Y-%m'),
                    'end': monthly_range[1].strftime('%Y-%m')
                }

            return verification

        finally:
            session.close()

    def verify_solar_energy_data(self):
        """Verify solar energy data loading"""
        if self.solar_energy_df is not None:
            logger.info(f"Solar energy data shape: {self.solar_energy_df.shape}")
            logger.info(f"Date range: {self.solar_energy_df['Date'].min()} to {self.solar_energy_df['Date'].max()}")
            logger.info(f"Sample values:\n{self.solar_energy_df.head()}")
            logger.info(f"Columns: {self.solar_energy_df.columns.tolist()}")
            
            # Check for any missing values
            nulls = self.solar_energy_df.isnull().sum()
            if nulls.any():
                logger.warning(f"Missing values found:\n{nulls[nulls > 0]}")