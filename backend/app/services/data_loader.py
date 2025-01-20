# backend/app/services/data_loader.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from ..models.water_consumption import Base, WaterConsumption
from .auckland_water_processor import AucklandWaterDataProcessor

class DataLoader:
    def __init__(self, db_url):
        """Initialize DataLoader with database connection"""
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_tables(self):
        """Create database tables"""
        Base.metadata.create_all(self.engine)

    def load_water_consumption_data(self, excel_file):
        """Load water consumption data from Excel to database"""
        try:
            # Initialize processor
            processor = AucklandWaterDataProcessor(excel_file)
            
            # Load and process data
            processor.load_data()
            processed_data = processor.process_data()
            
            # Convert processed data to database records
            records = []
            for _, row in processed_data.iterrows():
                record = WaterConsumption(
                    reading_date=row['Reading_Date'],
                    object_name=row['Object_Name'],
                    object_description=row['Object_Description'],
                    reading_description=row['Reading_Description'],
                    reading_value=row['Reading_Value']
                )
                records.append(record)
            
            # Bulk insert records
            self.session.bulk_save_objects(records)
            self.session.commit()
            
            return len(records)
            
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error loading data: {str(e)}")
        
        finally:
            self.session.close()