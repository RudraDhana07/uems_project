# backend/app/models/weather_models.py

from datetime import datetime
from .. import db

class WeatherDaily(db.Model):
    __tablename__ = 'weather_daily'
    __table_args__ = {'schema': 'dbo'}

    date_id = db.Column(db.Date, primary_key=True)
    temp_mean_working = db.Column(db.Float)
    temp_max_working = db.Column(db.Float)
    temp_min_working = db.Column(db.Float)
    temp_range_working = db.Column(db.Float)
    global_radiation_sum = db.Column(db.Float)
    peak_radiation = db.Column(db.Float)
    #solar_duration_hours = db.Column(db.Float) #not working
    wind_speed_mean = db.Column(db.Float)
    wind_direction_dominant = db.Column(db.Float)
    max_gust_speed = db.Column(db.Float)
    humidity_mean_working = db.Column(db.Float)
    humidity_range_working = db.Column(db.Float)
    morning_temp_mean = db.Column(db.Float)
    afternoon_temp_mean = db.Column(db.Float)
    evening_temp_mean = db.Column(db.Float)
    morning_humidity_mean = db.Column(db.Float)
    afternoon_humidity_mean = db.Column(db.Float)
    evening_humidity_mean = db.Column(db.Float)
    pressure_mean_working = db.Column(db.Float)
    rain_sum_working = db.Column(db.Float)
    season = db.Column(db.String(20))
    day_type = db.Column(db.String(50))
    academic_period = db.Column(db.String(50))
    weighted_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WeatherMonthly(db.Model):
    __tablename__ = 'weather_monthly'
    __table_args__ = {'schema': 'dbo'}

    month_id = db.Column(db.Date, primary_key=True)
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

    #total_solar_duration = db.Column(db.Float) # not working
    Mean_daily_Solar_energy = db.Column(db.Float)
    avg_wind_speed = db.Column(db.Float)
    morning_temp_mean = db.Column(db.Float)
    afternoon_temp_mean = db.Column(db.Float)
    evening_temp_mean = db.Column(db.Float)
    pressure_mean = db.Column(db.Float)

    weighted_monthly_score = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WeatherWeights(db.Model):
    __tablename__ = 'weather_weights'
    __table_args__ = {'schema': 'dbo'}

    season = db.Column(db.String(20), primary_key=True)
    temp_weight = db.Column(db.Float)
    radiation_weight = db.Column(db.Float)
    humidity_weight = db.Column(db.Float)
    wind_weight = db.Column(db.Float)
    term_multiplier = db.Column(db.Float)
    summer_break_multiplier = db.Column(db.Float)
    mid_sum_multiplier = db.Column(db.Float)
    exam_multiplier = db.Column(db.Float)
    public_multiplier = db.Column(db.Float)
    sunday_multiplier = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AcademicCalendar(db.Model):
    __tablename__ = 'academic_calendar'
    __table_args__ = {'schema': 'dbo'}

    date_id = db.Column(db.Date, primary_key=True)
    event_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    term_type = db.Column(db.String(50))
    season = db.Column(db.String(20))
    base_weight = db.Column(db.Float)
    seasonal_weight = db.Column(db.Float)
    day_type = db.Column(db.String(10))
    final_weight = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
