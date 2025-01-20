# backend/app/models/steam_mthw.py

from .. import db
from datetime import datetime

class SteamMTHWReading(db.Model):
    """Model for Steam and MTHW readings and consumption data"""
    __tablename__ = 'steam_mthw_readings'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(3), nullable=False)  # Three letter month abbreviation
    year = db.Column(db.Integer, nullable=False)
    
    # MTHW readings
    mthw_consumption_kwh = db.Column(db.Float)
    
    # 192 Castle readings and consumption
    castle_192_reading_kwh = db.Column(db.Float)
    castle_192_consumption_kwh = db.Column(db.Float)
    
    # Medical School Steam readings and consumption - Line A
    med_school_a_reading_kg = db.Column(db.Float)
    med_school_a_reading_kwh = db.Column(db.Float)
    med_school_a_consumption_kg = db.Column(db.Float)
    med_school_a_consumption_kwh = db.Column(db.Float)
    
    # Medical School Steam readings and consumption - Line B
    med_school_b_reading_kg = db.Column(db.Float)
    med_school_b_reading_kwh = db.Column(db.Float)
    med_school_b_consumption_kg = db.Column(db.Float)
    med_school_b_consumption_kwh = db.Column(db.Float)
    
    # Medical School total consumption
    med_school_consumption_kg = db.Column(db.Float)
    med_school_consumption_kwh = db.Column(db.Float)
    
    # Cumberland College readings and consumption
    cumberland_d401_dining_reading_kg = db.Column(db.Float)
    cumberland_d404_castle_reading_kg = db.Column(db.Float)
    cumberland_d401_d404_consumption_kg = db.Column(db.Float)
    cumberland_d401_d404_consumption_kwh = db.Column(db.Float)
    
    # Total Steam consumption
    total_steam_consumption_kwh = db.Column(db.Float)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert the model instance to a dictionary"""
        return {
            'id': self.id,
            'month': self.month,
            'year': self.year,
            'mthw_consumption_kwh': self.mthw_consumption_kwh,
            'castle_192_reading_kwh': self.castle_192_reading_kwh,
            'castle_192_consumption_kwh': self.castle_192_consumption_kwh,
            'med_school_a_reading_kg': self.med_school_a_reading_kg,
            'med_school_a_reading_kwh': self.med_school_a_reading_kwh,
            'med_school_a_consumption_kg': self.med_school_a_consumption_kg,
            'med_school_a_consumption_kwh': self.med_school_a_consumption_kwh,
            'med_school_b_reading_kg': self.med_school_b_reading_kg,
            'med_school_b_reading_kwh': self.med_school_b_reading_kwh,
            'med_school_b_consumption_kg': self.med_school_b_consumption_kg,
            'med_school_b_consumption_kwh': self.med_school_b_consumption_kwh,
            'med_school_consumption_kg': self.med_school_consumption_kg,
            'med_school_consumption_kwh': self.med_school_consumption_kwh,
            'cumberland_d401_dining_reading_kg': self.cumberland_d401_dining_reading_kg,
            'cumberland_d404_castle_reading_kg': self.cumberland_d404_castle_reading_kg,
            'cumberland_d401_d404_consumption_kg': self.cumberland_d401_d404_consumption_kg,
            'cumberland_d401_d404_consumption_kwh': self.cumberland_d401_d404_consumption_kwh,
            'total_steam_consumption_kwh': self.total_steam_consumption_kwh,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }