# backend/app/models/gas_models.py

from datetime import datetime
from .. import db

class GasAutomatedMeter(db.Model):
    __tablename__ = 'gas_automated_meter'
    __table_args__ = {'schema': 'dbo'}

    id = db.Column(db.Integer, primary_key=True)
    meter_description = db.Column(db.String(255))
    icp = db.Column(db.String(255))
    
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
    
    # 2025 monthly readings
    Jan_2025 = db.Column(db.Float)
    Feb_2025 = db.Column(db.Float)
    Mar_2025 = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'meter_description': self.meter_description,
            'icp': self.icp,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name)
               for col in self.__table__.columns
               if col.name not in ['id', 'meter_description', 'icp', 'created_at', 'updated_at']}
        }

class GasManualMeter(db.Model):
    __tablename__ = 'gas_manual_meter'
    __table_args__ = {'schema': 'dbo'}

    id = db.Column(db.Integer, primary_key=True)
    meter_description = db.Column(db.String(255))
    misc1 = db.Column(db.String(255))
    misc2 = db.Column(db.String(255))
    
    # Monthly readings columns same as above
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
    
    # 2025 monthly readings
    Jan_2025 = db.Column(db.Float)
    Feb_2025 = db.Column(db.Float)
    Mar_2025 = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'meter_description': self.meter_description,
            'misc1': self.misc1,
            'misc2': self.misc2,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name)
               for col in self.__table__.columns
               if col.name not in ['id', 'meter_description', 'misc1', 'misc2', 'created_at', 'updated_at']}
        }

class GasConsumption(db.Model):
    __tablename__ = 'gas_consumption'
    __table_args__ = {'schema': 'dbo'}

    id = db.Column(db.Integer, primary_key=True)
    object_description = db.Column(db.String(255))
    misc = db.Column(db.String(255))
    
    # Monthly readings columns same as above
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
    
    # 2025 monthly readings
    Jan_2025 = db.Column(db.Float)
    Feb_2025 = db.Column(db.Float)
    Mar_2025 = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'object_description': self.object_description,
            'misc': self.misc,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name)
               for col in self.__table__.columns
               if col.name not in ['id', 'object_description', 'misc', 'created_at', 'updated_at']}
        }
