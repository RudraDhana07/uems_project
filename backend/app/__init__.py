# backend/app/__init__.py

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Load environment variables
    load_dotenv()
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Import and register blueprints
    from .routes import auckland_routes, steam_mthw_routes, janitza_routes, lthw_routes, gas_routes, stream_elec_routes, cfi_routes, mthw_routes
    app.register_blueprint(auckland_routes.bp)
    app.register_blueprint(steam_mthw_routes.bp)
    app.register_blueprint(janitza_routes.bp)
    app.register_blueprint(lthw_routes.bp)
    app.register_blueprint(gas_routes.bp)
    app.register_blueprint(stream_elec_routes.bp) 
    app.register_blueprint(cfi_routes.bp) 
    app.register_blueprint(mthw_routes.bp) 
    
    # Create database tables
    with app.app_context():
        # Create schema if it doesn't exist
        db.session.execute(text('CREATE SCHEMA IF NOT EXISTS dbo'))
        db.session.commit()
        
        # Create all tables
        db.create_all()
    
    @app.route('/')
    def health_check():
        return {
            'status': 'healthy', 
            'message': 'UEMS API is running',
            'available_endpoints': [
                '/api/auckland/electricity',
                '/api/auckland/water-calculated',
                '/api/auckland/water',
                '/api/steam-mthw/readings',
                '/api/steam-mthw/readings/latest',
                '/api/steam-mthw/summary',
                '/api/janitza/med',
                '/api/janitza/freezer',
                '/api/janitza/uod4f6',
                '/api/janitza/uof8x',
                '/api/janitza/manual',
                '/api/janitza/calculated',
                '/api/lthw/automated',
                '/api/lthw/manual',
                '/api/lthw/consumption',
                '/api/gas/automated',
                '/api/gas/manual',
                '/api/gas/consumption',
                '/api/gas/analysis',
                '/api/stream-elec/ring-mains',
                '/api/stream-elec/libraries',
                '/api/stream-elec/colleges',
                '/api/stream-elec/science',
                '/api/stream-elec/health-science',
                '/api/stream-elec/humanities',
                '/api/stream-elec/obs-psychology',
                '/api/stream-elec/total-stream',
                '/api/stream-elec/its-servers',
                '/api/stream-elec/school-of-medicine',
                '/api/stream-elec/commerce',
                '/api/cfi/meter',
                '/api/cfi/rooms',
                '/api/mthw/meter',
                '/api/muthw/consumption'
            ]
        }
    
    return app
