# backend/app/routes/lthw_routes.py

from flask import Blueprint, jsonify
from ..models.lthw_models import (
    LTHWAutomatedMeter, LTHWManualMeter, LTHWConsumption
)
from .. import db
import logging

bp = Blueprint('lthw', __name__, url_prefix='/api/lthw')
logger = logging.getLogger(__name__)

@bp.route('/automated', methods=['GET'])
def get_automated_data():
    """Get LTHW automated meter data"""
    try:
        data = LTHWAutomatedMeter.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching LTHW automated data: {str(e)}")
        return jsonify({'error': 'Failed to fetch LTHW automated data'}), 500

@bp.route('/manual', methods=['GET'])
def get_manual_data():
    """Get LTHW manual meter data"""
    try:
        data = LTHWManualMeter.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching LTHW manual data: {str(e)}")
        return jsonify({'error': 'Failed to fetch LTHW manual data'}), 500

@bp.route('/consumption', methods=['GET'])
def get_consumption_data():
    """Get LTHW consumption data"""
    try:
        data = LTHWConsumption.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching LTHW consumption data: {str(e)}")
        return jsonify({'error': 'Failed to fetch LTHW consumption data'}), 500
