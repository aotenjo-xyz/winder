import logging
import os

class ColorFormatter(logging.Formatter):
    # Define the color codes
    COLORS = {
        logging.DEBUG: "\033[94m",    # Blue
        logging.INFO: "\033[92m",     # Green
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",    # Red
        logging.CRITICAL: "\033[95m", # Magenta
    }
    RESET = "\033[0m"  # Reset color

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        record.levelname = f"{color}{record.levelname:<8}{self.RESET}" # Pad to 8 characters
        # record.msg = f"{color}{record.msg}{self.RESET}"
        return super().format(record)


def init_logger():
	logger = logging.getLogger('Wind')
	debug_level = os.environ.get('DEBUG', '3')

	# Define the logging level based on the debug level
	if debug_level == '3':
		logging_level = logging.DEBUG
	elif debug_level == '2':
		logging_level = logging.INFO
	elif debug_level == '1':
		logging_level = logging.WARNING
	else:
		logging_level = logging.ERROR

	handler = logging.StreamHandler() 
	formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s	%(message)s') 
	handler.setFormatter(formatter)

	# Configure the logging
	logging.basicConfig(level=logging_level,
						# format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
						handlers=[handler])

	return logger

def load_config():
	import yaml
	config_path = 'settings.yml'
	if not os.path.exists(config_path):
		raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
	
	with open(config_path, 'r') as f:
		config = yaml.safe_load(f)
	return config