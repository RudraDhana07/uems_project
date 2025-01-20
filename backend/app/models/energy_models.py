# backend/app/models/energy_models.py
from .. import db
from datetime import datetime

class EnergyReading(db.Model):
    __tablename__ = 'energy_readings'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    energy_type = db.Column(db.String(50), nullable=False)  # MTHW, Steam, LPG, etc.
    division = db.Column(db.String(100))  # For different colleges, libraries
    building = db.Column(db.String(100))
    value = db.Column(db.Float, nullable=False)  # Reading value in kWh
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'energy_type': self.energy_type,
            'division': self.division,
            'building': self.building,
            'value': self.value,
            'created_at': self.created_at.isoformat()
        }

class Building(db.Model):
    __tablename__ = 'buildings'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    division = db.Column(db.String(100))
    location = db.Column(db.String(100))  # For AKL-WLG-CHC locations
    building_type = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'division': self.division,
            'location': self.location,
            'building_type': self.building_type
        }