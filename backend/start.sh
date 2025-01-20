# backend/start.sh
#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Export Flask environment variables
export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=1
export FLASK_RUN_PORT=5001

# Start Flask application
python -m flask run --port 5001