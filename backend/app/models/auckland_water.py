# backend/app/models/auckland_water.py

from .. import db
from datetime import datetime

class AucklandWaterCalculatedConsumption(db.Model):
    __tablename__ = 'auckland_water_calculated_consumption'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    meter_location = db.Column(db.String(255))
    object_name = db.Column(db.String(255))
    object_description = db.Column(db.String(255))
    
    # Monthly readings starting from December 2021
    Dec_2021 = db.Column(db.Float)

    # 2022 monthly readings
    Jan_2022 = db.Column(db.Float)
    Feb_2022 = db.Column(db.Float)
    Mar_2022 = db.Column(db.Float)
    Apr_2022 = db.Column(db.Float)
    May_2022 = db.Column(db.Float)
    Jun_2022 = db.Column(db.Float)
    Jul_2022 = db.Column(db.Float)
    Aug_2022 = db.Column(db.Float)
    Sep_2022 = db.Column(db.Float)
    Oct_2022 = db.Column(db.Float)
    Nov_2022 = db.Column(db.Float)
    Dec_2022 = db.Column(db.Float)
    
    # 2023 monthly readings
    Jan_2023 = db.Column(db.Float)
    Feb_2023 = db.Column(db.Float)
    Mar_2023 = db.Column(db.Float)
    Apr_2023 = db.Column(db.Float)
    May_2023 = db.Column(db.Float)
    Jun_2023 = db.Column(db.Float)
    Jul_2023 = db.Column(db.Float)
    Aug_2023 = db.Column(db.Float)
    Sep_2023 = db.Column(db.Float)
    Oct_2023 = db.Column(db.Float)
    Nov_2023 = db.Column(db.Float)
    Dec_2023 = db.Column(db.Float)
    
    # 2024 monthly readings
    Jan_2024 = db.Column(db.Float)
    Feb_2024 = db.Column(db.Float)
    Mar_2024 = db.Column(db.Float)
    Apr_2024 = db.Column(db.Float)
    May_2024 = db.Column(db.Float)
    Jun_2024 = db.Column(db.Float)
    Jul_2024 = db.Column(db.Float)
    Aug_2024 = db.Column(db.Float)
    Sep_2024 = db.Column(db.Float)
    Oct_2024 = db.Column(db.Float)
    Nov_2024 = db.Column(db.Float)
    Dec_2024 = db.Column(db.Float)
    
    # 2025 monthly readings (Jan through Mar)
    Jan_2025 = db.Column(db.Float)
    Feb_2025 = db.Column(db.Float)
    Mar_2025 = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'object_name': self.object_name,
            'object_description': self.object_description,
            'meter_location': self.meter_location,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name) 
               for col in self.__table__.columns 
               if col.name not in ['id', 'object_name', 'object_description', 
                                 'meter_location', 'created_at', 'updated_at']}
        }

class AucklandWaterConsumption(db.Model):
    __tablename__ = 'auckland_water_consumption'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    reading_description = db.Column(db.String(500))
    object_name = db.Column(db.String(255))
    object_description = db.Column(db.String(255))
   
    # Monthly readings starting from December 2021
    Dec_2021 = db.Column(db.Float)
    
    # 2022 monthly readings
    Jan_2022 = db.Column(db.Float)
    Feb_2022 = db.Column(db.Float)
    Mar_2022 = db.Column(db.Float)
    Apr_2022 = db.Column(db.Float)
    May_2022 = db.Column(db.Float)
    Jun_2022 = db.Column(db.Float)
    Jul_2022 = db.Column(db.Float)
    Aug_2022 = db.Column(db.Float)
    Sep_2022 = db.Column(db.Float)
    Oct_2022 = db.Column(db.Float)
    Nov_2022 = db.Column(db.Float)
    Dec_2022 = db.Column(db.Float)
    
    # 2023 monthly readings
    Jan_2023 = db.Column(db.Float)
    Feb_2023 = db.Column(db.Float)
    Mar_2023 = db.Column(db.Float)
    Apr_2023 = db.Column(db.Float)
    May_2023 = db.Column(db.Float)
    Jun_2023 = db.Column(db.Float)
    Jul_2023 = db.Column(db.Float)
    Aug_2023 = db.Column(db.Float)
    Sep_2023 = db.Column(db.Float)
    Oct_2023 = db.Column(db.Float)
    Nov_2023 = db.Column(db.Float)
    Dec_2023 = db.Column(db.Float)
    
    # 2024 monthly readings
    Jan_2024 = db.Column(db.Float)
    Feb_2024 = db.Column(db.Float)
    Mar_2024 = db.Column(db.Float)
    Apr_2024 = db.Column(db.Float)
    May_2024 = db.Column(db.Float)
    Jun_2024 = db.Column(db.Float)
    Jul_2024 = db.Column(db.Float)
    Aug_2024 = db.Column(db.Float)
    Sep_2024 = db.Column(db.Float)
    Oct_2024 = db.Column(db.Float)
    Nov_2024 = db.Column(db.Float)
    Dec_2024 = db.Column(db.Float)
    
    # 2025 monthly readings (Jan through Mar)
    Jan_2025 = db.Column(db.Float)
    Feb_2025 = db.Column(db.Float)
    Mar_2025 = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'object_name': self.object_name,
            'object_description': self.object_description,
            'reading_description': self.reading_description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name) 
               for col in self.__table__.columns 
               if col.name not in ['id', 'object_name', 'object_description', 
                                 'reading_description', 'created_at', 'updated_at']}
        }