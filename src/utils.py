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


def get_winding_teeth_indices(winding_config: str):
    """
    Get winding teeth indices from winding configuration string.
    You can find the winding configuration string on [our website](https://aotenjo.xyz/docs/winder/winding-config/)

    Example: "AaAabBbBCcCcaAaABbBbcCcC" for 24n22p motor (24 slots, 22 poles)
    """
    only_small_letters = winding_config.lower()
    teeth_indices_a = []
    teeth_indices_b = []
    teeth_indices_c = []
    for i, letter in enumerate(only_small_letters):
        if letter == "a":
            teeth_indices_a.append(i)
        elif letter == "b":
            teeth_indices_b.append(i)
        elif letter == "c":
            teeth_indices_c.append(i)
    teeth_index_matrix = [teeth_indices_a, teeth_indices_b, teeth_indices_c]

    return teeth_index_matrix


def is_clockwise(winding_config: str, teeth_idx: int):
    letter = winding_config[teeth_idx]
    return letter.islower()


def get_num_of_tooth_to_wind(winding_config: str):
    # Assuming the winding configuration is valid and has 3 wires, the number of teeth to wind for each wire can be calculated as the total length of the winding configuration divided by 3.
    if len(winding_config) % 3 != 0:
        raise ValueError("Winding configuration length must be a multiple of 3.")
    return len(winding_config) // 3


def is_starting_from_bottom(starts_at: int, winding_config: str, teeth_indices) -> bool:
    """
    Determine if the winding starts from the bottom based on the starting position and wire index.
    """
    if starts_at == 0:
        return False
    teeth_idx = teeth_indices[starts_at]
    prev_teeth_idx = teeth_indices[starts_at - 1]
    if teeth_idx - prev_teeth_idx != 1:
        return False

    return is_clockwise(winding_config, prev_teeth_idx)


def get_current_teeth(motor1_pos, m1_zero, teeth_count):
    diff = abs(m1_zero - motor1_pos)
    teeth_number = int(round(diff / ((math.pi * 2) / teeth_count)))
    if teeth_number >= teeth_count:
        return teeth_number % teeth_count
    return teeth_number


def is_skipping(winding_config: str, teeth_idx: int):
    winding_config = (
        winding_config.lower()
    )  # Convert to lowercase for case-insensitive comparison
    # get first index of the current character in the winding configuration
    # e.g. when winding_config = "AaAabBbBCcCcaAaABbBbcCcC", the first index of 'a' is 0, the first index of 'b' is 4, the first index of 'c' is 9
    starting_char = winding_config[teeth_idx]
    starting_char_first_index = winding_config.index(starting_char)
    if teeth_idx == starting_char_first_index:
        return False
    current_char = winding_config[teeth_idx]
    prev_char = winding_config[teeth_idx - 1]
    return current_char.lower() != prev_char.lower()
