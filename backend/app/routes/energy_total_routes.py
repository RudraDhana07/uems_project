# backend/app/routes/energy_total_routes.py

from flask import Blueprint, jsonify
from ..models.energy_total_models import EnergyTotalDashboard
from .. import db
import logging
from sqlalchemy import desc

bp = Blueprint('energy_total', __name__, url_prefix='/api/energy-total')
logger = logging.getLogger(__name__)

# backend/app/routes/energy_total_routes.py

@bp.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get all energy total dashboard data"""
    try:
        logger.info("Starting to fetch dashboard data")
        data = EnergyTotalDashboard.query.all()
        result = [record.to_dict() for record in data]
        logger.info(f"Successfully fetched {len(result)} records")
        logger.debug(f"Data: {result}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error fetching energy dashboard data: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        return jsonify({'error': 'Failed to fetch energy dashboard data'}), 500


@bp.route('/latest', methods=['GET'])
def get_latest_readings():
    """Get the most recent energy readings"""
    try:
        latest = EnergyTotalDashboard.query.order_by(
            EnergyTotalDashboard.year.desc(),
            EnergyTotalDashboard.month.desc()
        ).first()
        return jsonify(latest.to_dict() if latest else {})
    except Exception as e:
        logger.error(f"Error fetching latest energy data: {str(e)}")
        return jsonify({'error': 'Failed to fetch latest energy data'}), 500

@bp.route('/year/<int:year>', methods=['GET'])
def get_readings_by_year(year):
    """Get energy readings for a specific year"""
    try:
        data = EnergyTotalDashboard.query.filter_by(year=year).order_by(
            EnergyTotalDashboard.month.asc()
        ).all()
        return jsonify([reading.to_dict() for reading in data])
    except Exception as e:
        logger.error(f"Error fetching energy data for year {year}: {str(e)}")
        return jsonify({'error': f'Failed to fetch energy data for year {year}'}), 500

@bp.route('/summary', methods=['GET'])
def get_summary():
    """Get summary statistics for total energy consumption"""
    try:
        latest_year = db.session.query(db.func.max(EnergyTotalDashboard.year)).scalar()
        
        summary = {
            'total_electricity': db.session.query(
                db.func.sum(EnergyTotalDashboard.total_stream_dn_electricity_kwh)
            ).filter_by(year=latest_year).scalar(),
            'total_mthw': db.session.query(
                db.func.sum(EnergyTotalDashboard.mthw_kwh)
            ).filter_by(year=latest_year).scalar(),
            'total_steam': db.session.query(
                db.func.sum(EnergyTotalDashboard.steam_kwh)
            ).filter_by(year=latest_year).scalar(),
            'total_lpg': db.session.query(
                db.func.sum(EnergyTotalDashboard.lpg_kwh)
            ).filter_by(year=latest_year).scalar(),
            'total_woodchip': db.session.query(
                db.func.sum(EnergyTotalDashboard.woodchip_pellet_kwh)
            ).filter_by(year=latest_year).scalar(),
            'total_solar': db.session.query(
                db.func.sum(EnergyTotalDashboard.solar_kwh)
            ).filter_by(year=latest_year).scalar(),
            'total_energy': db.session.query(
                db.func.sum(EnergyTotalDashboard.total_kwh)
            ).filter_by(year=latest_year).scalar(),
            'year': latest_year
        }
        return jsonify(summary)
    except Exception as e:
        logger.error(f"Error fetching energy summary: {str(e)}")
        return jsonify({'error': 'Failed to fetch energy summary'}), 500


@bp.route('/analytics', methods=['GET'])
def get_analytics_data():
    try:
        data = EnergyTotalDashboard.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching analytics data: {str(e)}")
        return jsonify({'error': 'Failed to fetch analytics data'}), 500