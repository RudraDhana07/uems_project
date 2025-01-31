# backend/app/models/weather_models_monthly.py

from datetime import datetime
from .. import db

class WeatherMonthly(db.Model):
    __tablename__ = 'weather_matrics_monthly'
    __table_args__ = {'schema': 'dbo'}

    id = db.Column(db.Integer, primary_key=True)
    Year_value = db.Column(db.Float)
    Month_value = db.Column(db.String(255))
    temp_mean = db.Column(db.Float)
    temp_max = db.Column(db.Float)
    temp_min = db.Column(db.Float)
    temp_std_dev = db.Column(db.Float)
    radiation_total = db.Column(db.Float)
    avg_peak_radiation = db.Column(db.Float)
    humidity_mean = db.Column(db.Float)
    rain_total = db.Column(db.Float)
    term_days = db.Column(db.Integer)
    holiday_days = db.Column(db.Integer)
    exam_days = db.Column(db.Integer)

    Mean_daily_Solar_energy = db.Column(db.Float)
    avg_wind_speed = db.Column(db.Float)
    morning_temp_mean = db.Column(db.Float)
    afternoon_temp_mean = db.Column(db.Float)
    evening_temp_mean = db.Column(db.Float)
    pressure_mean = db.Column(db.Float)
    
    weighted_monthly_score = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

