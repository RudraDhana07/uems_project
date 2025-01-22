# backend/app/routes/gas_routes.py

from flask import Blueprint, jsonify
from ..models.gas_models import (
    GasAutomatedMeter, GasManualMeter, GasConsumption
)
from .. import db
import logging

bp = Blueprint('gas', __name__, url_prefix='/api/gas')
logger = logging.getLogger(__name__)

@bp.route('/automated', methods=['GET'])
def get_automated_data():
    """Get Gas automated meter data"""
    try:
        data = GasAutomatedMeter.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Gas automated data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Gas automated data'}), 500

@bp.route('/manual', methods=['GET'])
def get_manual_data():
    """Get Gas manual meter data"""
    try:
        data = GasManualMeter.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Gas manual data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Gas manual data'}), 500

@bp.route('/consumption', methods=['GET'])
def get_consumption_data():
    """Get Gas consumption data"""
    try:
        data = GasConsumption.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Gas consumption data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Gas consumption data'}), 500
