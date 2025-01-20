# backend/app/routes/steam_mthw_routes.py
from flask import Blueprint, jsonify
from ..models.steam_mthw import SteamMTHWReading
from .. import db
import logging
import math
from sqlalchemy import desc

bp = Blueprint('steam_mthw', __name__, url_prefix='/api/steam-mthw')
logger = logging.getLogger(__name__)

@bp.route('/readings', methods=['GET'])
def get_readings():
    try:
        data = SteamMTHWReading.query.all()
        readings = []
        for reading in data:
            reading_dict = reading.to_dict()
            # Convert NaN to None for JSON serialization
            for key, value in reading_dict.items():
                if isinstance(value, float) and math.isnan(value):
                    reading_dict[key] = None
            readings.append(reading_dict)
        return jsonify(readings)
    except Exception as e:
        logger.error(f"Error fetching Steam and MTHW data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/readings/latest', methods=['GET'])
def get_latest_readings():
    """Get the most recent Steam and MTHW readings"""
    try:
        latest = SteamMTHWReading.query.order_by(
            SteamMTHWReading.year.desc(),
            SteamMTHWReading.month.desc()
        ).first()
        return jsonify(latest.to_dict() if latest else {})
    except Exception as e:
        logger.error(f"Error fetching latest Steam and MTHW data: {str(e)}")
        return jsonify({'error': 'Failed to fetch latest Steam and MTHW data'}), 500

@bp.route('/readings/<int:year>', methods=['GET'])  # Changed to include year parameter
def get_readings_by_year(year):
    """Get Steam and MTHW readings for a specific year"""
    try:
        data = SteamMTHWReading.query.filter_by(year=year).order_by(
            SteamMTHWReading.month.asc()
        ).all()
        return jsonify([reading.to_dict() for reading in data])
    except Exception as e:
        logger.error(f"Error fetching Steam and MTHW data for year {year}: {str(e)}")
        return jsonify({'error': f'Failed to fetch Steam and MTHW data for year {year}'}), 500

@bp.route('/summary', methods=['GET'])
def get_summary():
    """Get summary statistics for Steam and MTHW data"""
    try:
        # Get the most recent complete year's data
        latest_year = db.session.query(db.func.max(SteamMTHWReading.year)).scalar()
        summary = {
            'total_mthw_consumption': db.session.query(
                db.func.sum(SteamMTHWReading.mthw_consumption_kwh)
            ).filter_by(year=latest_year).scalar(),
            'total_steam_consumption': db.session.query(
                db.func.sum(SteamMTHWReading.total_steam_consumption_kwh)
            ).filter_by(year=latest_year).scalar(),
            'med_school_consumption': db.session.query(
                db.func.sum(SteamMTHWReading.med_school_consumption_kwh)
            ).filter_by(year=latest_year).scalar(),
            'cumberland_consumption': db.session.query(
                db.func.sum(SteamMTHWReading.cumberland_d401_d404_consumption_kwh)
            ).filter_by(year=latest_year).scalar(),
            'year': latest_year
        }
        return jsonify(summary)
    except Exception as e:
        logger.error(f"Error fetching Steam and MTHW summary: {str(e)}")
        return jsonify({'error': 'Failed to fetch Steam and MTHW summary'}), 500
