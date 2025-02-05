# In root/app.py
from backend.app import create_app
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Starting app creation")
app = create_app()
logger.debug("App created successfully")

if __name__ == "__main__":
    app.run()