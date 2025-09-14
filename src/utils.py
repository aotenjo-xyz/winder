import logging
import os
import math

class ColorFormatter(logging.Formatter):
    # Define the color codes
    COLORS = {
        logging.DEBUG: "\033[94m",  # Blue
        logging.INFO: "\033[92m",  # Green
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[95m",  # Magenta
    }
    RESET = "\033[0m"  # Reset color

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        record.levelname = (
            f"{color}{record.levelname:<8}{self.RESET}"  # Pad to 8 characters
        )
        # record.msg = f"{color}{record.msg}{self.RESET}"
        return super().format(record)


def init_logger():
    logger = logging.getLogger("Wind")
    debug_level = os.environ.get("DEBUG", "3")

    # Define the logging level based on the debug level
    if debug_level == "3":
        logging_level = logging.DEBUG
    elif debug_level == "2":
        logging_level = logging.INFO
    elif debug_level == "1":
        logging_level = logging.WARNING
    else:
        logging_level = logging.ERROR

    handler = logging.StreamHandler()
    formatter = ColorFormatter("%(asctime)s - %(name)s - %(levelname)s	%(message)s")
    handler.setFormatter(formatter)

    # Configure the logging
    logging.basicConfig(
        level=logging_level,
        # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[handler],
    )

    return logger


def load_config(config_path):
    import yaml

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config


def get_wind_orders_and_slot_indices(winding_config: str):
    """
    Get winding orders and slot indices from winding configuration string.
    You can find the winding configuration string at [Winding Scheme Calculator](https://www.bavaria-direct.co.za/scheme/calculator/)

    Example: "AaAabBbBCcCcaAaABbBbcCcC" for 24n22p motor (24 slots, 22 poles)
    """
    only_small_letters = winding_config.lower()
    slot_indices_a = []
    slot_indices_b = []
    slot_indices_c = []
    for i, letter in enumerate(only_small_letters):
        if letter == "a":
            slot_indices_a.append(i)
        elif letter == "b":
            slot_indices_b.append(i)
        elif letter == "c":
            slot_indices_c.append(i)
    slot_index_matrix = [slot_indices_a, slot_indices_b, slot_indices_c]

    wind_orders = []
    for slot_indices in slot_index_matrix:
        wind_order = []
        for slot_idx in slot_indices:
            letter = winding_config[slot_idx]
            if letter.isupper():
                wind_order.append(0)
            else:
                wind_order.append(1)
        wind_orders.append(wind_order)
    return wind_orders, slot_index_matrix


def get_current_slot(motor1_pos, m1_zero, slot_count):
    diff = abs(m1_zero - motor1_pos)
    slot_number = int(round(diff / ((math.pi * 2) / slot_count)))
    if slot_number >= slot_count:
        return slot_number % slot_count
    return slot_number