from flask import Blueprint, jsonify, current_app
from ..models.cfi_models import CenterForInnovation, CfiRoomTypes
from .. import db
import logging

bp = Blueprint('cfi', __name__, url_prefix='/api/cfi')
logger = logging.getLogger(__name__)

@bp.route('/meter', methods=['GET'])
def get_meter_data():
    """Get Center for Innovation meter data"""
    try:
        data = CenterForInnovation.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        return jsonify({'error': 'Failed to fetch CFI meter data'}), 500

@bp.route('/rooms', methods=['GET'])
def get_room_data():
    """Get CFI room types data"""
    try:
        data = CfiRoomTypes.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        return jsonify({'error': 'Failed to fetch CFI room data'}), 500
