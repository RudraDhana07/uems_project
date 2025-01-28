# backend/app/models/energy_total_models.py

from datetime import datetime
from .. import db

class EnergyTotalDashboard(db.Model):
    __tablename__ = 'energy_total_dashboard'
    __table_args__ = {'schema': 'dbo'}

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(3), nullable=False)  # Three letter month abbreviation
    year = db.Column(db.Integer, nullable=False)
    total_stream_dn_electricity_kwh = db.Column(db.Float)
    mthw_kwh = db.Column(db.Float)
    steam_kwh = db.Column(db.Float)
    lpg_kwh = db.Column(db.Float)
    woodchip_pellet_kwh = db.Column(db.Float)
    solar_kwh = db.Column(db.Float)
    total_kwh = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert the model instance to a dictionary"""
        return {
            'id': self.id,
            'month': self.month,
            'year': self.year,
            'total_stream_dn_electricity_kwh': self.total_stream_dn_electricity_kwh,
            'mthw_kwh': self.mthw_kwh,
            'steam_kwh': self.steam_kwh,
            'lpg_kwh': self.lpg_kwh,
            'woodchip_pellet_kwh': self.woodchip_pellet_kwh,
            'solar_kwh': self.solar_kwh,
            'total_kwh': self.total_kwh,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
