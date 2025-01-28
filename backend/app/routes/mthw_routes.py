# backend/app/routes/mthw_routes.py

from flask import Blueprint, jsonify
from ..models.mthw_models import MTHWMeterReading, MTHWConsumptionReading
from .. import db
import logging

bp = Blueprint('mthw', __name__, url_prefix='/api/mthw')
logger = logging.getLogger(__name__)

@bp.route('/meter', methods=['GET'])
def get_meter_data():
    """Get MTHW meter reading data"""
    try:
        data = MTHWMeterReading.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching MTHW meter reading data: {str(e)}")
        return jsonify({'error': 'Failed to fetch MTHW meter reading data'}), 500

@bp.route('/consumption', methods=['GET'])
def get_consumption_data():
    """Get MTHW consumption reading data"""
    try:
        data = MTHWConsumptionReading.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching MTHW consumption data: {str(e)}")
        return jsonify({'error': 'Failed to fetch MTHW consumption data'}), 500
