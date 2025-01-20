# backend/app/routes/energy_routes.py
from flask import Blueprint, jsonify, request
from ..models.energy_models import EnergyReading, Building
from .. import db

bp = Blueprint('energy', __name__, url_prefix='/api')

@bp.route('/energy/total', methods=['GET'])
def get_energy_total():
    """Get total energy consumption data"""
    readings = EnergyReading.query.all()
    return jsonify([reading.to_dict() for reading in readings])

@bp.route('/energy/by-type/<energy_type>', methods=['GET'])
def get_energy_by_type(energy_type):
    """Get energy consumption data for a specific type"""
    readings = EnergyReading.query.filter_by(energy_type=energy_type).all()
    return jsonify([reading.to_dict() for reading in readings])

@bp.route('/energy/by-division/<division>', methods=['GET'])
def get_energy_by_division(division):
    """Get energy consumption data for a specific division"""
    readings = EnergyReading.query.filter_by(division=division).all()
    return jsonify([reading.to_dict() for reading in readings])

@bp.route('/buildings', methods=['GET'])
def get_buildings():
    """Get all buildings"""
    buildings = Building.query.all()
    return jsonify([building.to_dict() for building in buildings])