# backend/app/routes/auckland_routes.py

from flask import Blueprint, jsonify
from ..models.auckland_electricity import AucklandElectricityCalculatedConsumption
from ..models.auckland_water import AucklandWaterCalculatedConsumption, AucklandWaterConsumption
import logging

bp = Blueprint('auckland', __name__, url_prefix='/api/auckland')
logger = logging.getLogger(__name__)

@bp.route('/electricity', methods=['GET'])
def get_electricity_data():
    """Get electricity consumption data"""
    try:
        data = AucklandElectricityCalculatedConsumption.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching electricity data: {str(e)}")
        return jsonify({'error': 'Failed to fetch electricity data'}), 500

@bp.route('/water-calculated', methods=['GET'])
def get_water_calculated_data():
    """Get calculated water consumption data"""
    try:
        data = AucklandWaterCalculatedConsumption.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching calculated water data: {str(e)}")
        return jsonify({'error': 'Failed to fetch calculated water data'}), 500

@bp.route('/water', methods=['GET'])
def get_water_data():
    """Get water consumption data"""
    try:
        data = AucklandWaterConsumption.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching water data: {str(e)}")
        return jsonify({'error': 'Failed to fetch water data'}), 500