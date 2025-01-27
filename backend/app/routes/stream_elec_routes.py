# backend/app/routes/stream_elec_routes.py

from flask import Blueprint, jsonify
from ..models.stream_elec_models import (
    RingMainsStream, LibrariesStream, CollegesStream,
    ScienceStream, HealthScienceStream, HumanitiesStream,
    ObsPsychologyStream, TotalStreamDnElectricity,
    ItsServersStream, SchoolOfMedicineChChStream, CommerceStream
)
from .. import db
import logging

bp = Blueprint('stream_elec', __name__, url_prefix='/api/stream-elec')
logger = logging.getLogger(__name__)

@bp.route('/ring-mains', methods=['GET'])
def get_ring_mains_data():
    """Get Ring Mains stream data"""
    try:
        data = RingMainsStream.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Ring Mains data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Ring Mains data'}), 500

@bp.route('/libraries', methods=['GET'])
def get_libraries_data():
    """Get Libraries stream data"""
    try:
        data = LibrariesStream.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Libraries data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Libraries data'}), 500

@bp.route('/colleges', methods=['GET'])
def get_colleges_data():
    """Get Colleges stream data"""
    try:
        data = CollegesStream.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Colleges data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Colleges data'}), 500

@bp.route('/science', methods=['GET'])
def get_science_data():
    """Get Science stream data"""
    try:
        data = ScienceStream.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Science data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Science data'}), 500

@bp.route('/health-science', methods=['GET'])
def get_health_science_data():
    """Get Health Science stream data"""
    try:
        data = HealthScienceStream.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Health Science data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Health Science data'}), 500

@bp.route('/humanities', methods=['GET'])
def get_humanities_data():
    """Get Humanities stream data"""
    try:
        data = HumanitiesStream.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Humanities data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Humanities data'}), 500

@bp.route('/obs-psychology', methods=['GET'])
def get_obs_psychology_data():
    """Get OBS Psychology stream data"""
    try:
        data = ObsPsychologyStream.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching OBS Psychology data: {str(e)}")
        return jsonify({'error': 'Failed to fetch OBS Psychology data'}), 500

@bp.route('/total-stream', methods=['GET'])
def get_total_stream_data():
    """Get Total Stream DN Electricity data"""
    try:
        data = TotalStreamDnElectricity.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Total Stream data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Total Stream data'}), 500

@bp.route('/its-servers', methods=['GET'])
def get_its_servers_data():
    """Get ITS Servers stream data"""
    try:
        data = ItsServersStream.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching ITS Servers data: {str(e)}")
        return jsonify({'error': 'Failed to fetch ITS Servers data'}), 500

@bp.route('/school-of-medicine', methods=['GET'])
def get_school_of_medicine_data():
    """Get School of Medicine ChCh stream data"""
    try:
        data = SchoolOfMedicineChChStream.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching School of Medicine data: {str(e)}")
        return jsonify({'error': 'Failed to fetch School of Medicine data'}), 500

@bp.route('/commerce', methods=['GET'])
def get_commerce_data():
    """Get Commerce stream data"""
    try:
        data = CommerceStream.query.all()
        return jsonify([record.to_dict() for record in data])
    except Exception as e:
        logger.error(f"Error fetching Commerce data: {str(e)}")
        return jsonify({'error': 'Failed to fetch Commerce data'}), 500
