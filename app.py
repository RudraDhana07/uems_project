# root/app.py
import os
import sys
import logging
from datetime import datetime
from backend.app import create_app

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Log environment information
try:
    # Log system information
    logger.info(f"Starting UEMS API Application at {datetime.now().isoformat()}")
    logger.info(f"Working Directory: {os.getcwd()}")
    logger.info(f"Directory Contents: {os.listdir('.')}")
    logger.info(f"Python Path: {sys.path}")
    logger.info(f"Environment: {'Production' if os.environ.get('WEBSITE_HOSTNAME') else 'Development'}")

    # Create Flask application
    logger.debug("Starting app creation")
    app = create_app()
    logger.debug("App created successfully")

    # Add basic health check endpoint
    @app.route('/health')
    def health_check():
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'environment': 'Production' if os.environ.get('WEBSITE_HOSTNAME') else 'Development',
            'app_directory': os.getcwd()
        }

except Exception as e:
    logger.error(f"Failed to initialize application: {str(e)}", exc_info=True)
    raise

if __name__ == "__main__":
    app.run()
