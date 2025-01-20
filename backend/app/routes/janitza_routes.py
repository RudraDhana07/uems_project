# backend/app/routes/janitza_routes.py
from flask import Blueprint, jsonify
from ..models.janitza_models import (
    JanitzaMedData, JanitzaFreezerRoom, JanitzaUOD4F6,
    JanitzaUOF8X, JanitzaManualMeters, JanitzaCalculatedConsumption
)
from .. import db
import logging

bp = Blueprint('janitza', __name__, url_prefix='/api/janitza')
logger = logging.getLogger(__name__)

@bp.route('/med', methods=['GET'])
def get_med_data():
    """Get Janitza medical data"""
    try:
        data = JanitzaMedData.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Janitza med data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Janitza med data'}), 500

@bp.route('/freezer', methods=['GET'])
def get_freezer_data():
    """Get Janitza freezer room data"""
    try:
        data = JanitzaFreezerRoom.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Janitza freezer data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Janitza freezer data'}), 500

@bp.route('/uod4f6', methods=['GET'])
def get_uod4f6_data():
    """Get Janitza UO D4-F6 data"""
    try:
        data = JanitzaUOD4F6.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Janitza UO D4-F6 data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Janitza UO D4-F6 data'}), 500

@bp.route('/uof8x', methods=['GET'])
def get_uof8x_data():
    """Get Janitza UO F8-X data"""
    try:
        data = JanitzaUOF8X.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Janitza UO F8-X data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Janitza UO F8-X data'}), 500

@bp.route('/manual', methods=['GET'])
def get_manual_data():
    """Get Janitza manual meters data"""
    try:
        data = JanitzaManualMeters.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Janitza manual meters data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Janitza manual meters data'}), 500

@bp.route('/calculated', methods=['GET'])
def get_calculated_data():
    """Get Janitza calculated consumption data"""
    try:
        data = JanitzaCalculatedConsumption.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Janitza calculated data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Janitza calculated data'}), 500
