# backend/app/routes/energy_total_routes.py

from flask import Blueprint, jsonify
from ..models.energy_total_models import EnergyTotalDashboard
from .. import db
import logging

bp = Blueprint('energy_total', __name__, url_prefix='/api/energy-total')
logger = logging.getLogger(__name__)

@bp.route('/', methods=['GET'])
def get_energy_total():
    """Get all energy total dashboard data"""
    try:
        data = EnergyTotalDashboard.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching energy total data: {str(e)}")
        return jsonify({'error': 'Failed to fetch energy total data'}), 500

@bp.route('/<int:year>/<string:month>', methods=['GET'])
def get_energy_by_month(year, month):
    """Get energy total data for specific month and year"""
    try:
        record = EnergyTotalDashboard.query.filter_by(
            year=year,
            month=month
        ).first()
        
        if not record:
            return jsonify({'error': 'No data found for specified period'}), 404
            
        return jsonify(record.to_dict())
    except Exception as e:
        logger.error(f"Error fetching energy data for {month} {year}: {str(e)}")
        return jsonify({'error': 'Failed to fetch energy data'}), 500
