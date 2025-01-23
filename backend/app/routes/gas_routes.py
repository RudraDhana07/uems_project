# backend/app/routes/gas_routes.py

from flask import Blueprint, jsonify
from ..models.gas_models import GasAutomatedMeter, GasManualMeter, GasConsumption
from ..services.gas_analysis_service import GasAnalysisService
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

@bp.route('/analysis', methods=['GET'])
def get_gas_analysis():
    try:
        logger.info("Starting gas analysis request")
        analysis_service = GasAnalysisService(db)
        analysis_results = analysis_service.get_analysis_data()
        
        if not analysis_results or 'error' in analysis_results:
            logger.error(f"Analysis returned no results or error: {analysis_results}")
            return jsonify({
                'error': 'No analysis results available',
                'details': analysis_results.get('error', 'Unknown error')
            }), 404
        
        # Process consumption patterns
        if 'consumption_patterns' in analysis_results:
            for pattern in analysis_results['consumption_patterns']:
                pattern['consumption_pattern'] = {
                    k: round(float(v), 2) if v is not None else 0
                    for k, v in pattern['consumption_pattern'].items()
                }
        
        logger.info(f"Analysis completed successfully: {len(analysis_results.get('cluster_results', []))} clusters found")
        return jsonify(analysis_results)
    
    except Exception as e:
        logger.exception("Error in gas analysis route")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500