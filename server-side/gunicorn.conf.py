# gunicorn.conf.py

import logging

# Define custom log format
access_log_format = (
    '"%(r)s" %(s)s %(B)s "%(f)s" "%(a)s"'
)

# Access log configuration
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr

# Adjust log level if needed
loglevel = 'info'

# Logger setup to include custom formatting
logger_class = 'gunicorn.glogging.Logger'
