# logger.py
import logging
import warnings

# Create a custom logger
logger = logging.getLogger('app_logger')
logger.setLevel(logging.DEBUG)  # Capture DEBUG and above levels

# Create file handler for both logs and exceptions
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# Create formatters and add them to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handler to the logger
logger.addHandler(file_handler)

# Configure warnings to log as well
def custom_warning_handler(message, category, filename, lineno, file=None, line=None):
    logger.warning(f'{filename}:{lineno}: {category.__name__}: {message}')

# Redirect warnings to the logger
warnings.showwarning = custom_warning_handler
