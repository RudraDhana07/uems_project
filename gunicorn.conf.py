# gunicorn.conf.py
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = 4
worker_class = 'sync'
worker_connections = 1000
timeout = 300
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True

# Process naming
proc_name = 'uems_api'

# Directory
chdir = os.getenv('APP_PATH', '/home/site/wwwroot')
