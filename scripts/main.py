from src.winding import Wind
from time import sleep
import sys
import termios
import tty
from typing import Sequence


def _prompt_choice(prompt: str, valid_choices: set[str]) -> str:
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"Invalid choice: {choice}. Please choose one of {sorted(valid_choices)}")


def _read_key() -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            ch2 = sys.stdin.read(1)
            if ch2 == "[":
                ch3 = sys.stdin.read(1)
                return f"\x1b[{ch3}"
            return ch + ch2
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def _arrow_select_option(title: str, options: Sequence[tuple[str, str]]) -> str:
    selected_idx = 0
    print(f"\n{title}")
    print("Use Up/Down arrows and Enter to select.")

    while True:
        for idx, (_, label) in enumerate(options):
            prefix = ">" if idx == selected_idx else " "
            print(f" {prefix} {label}")

        key = _read_key()
        if key == "\x1b[A":
            selected_idx = (selected_idx - 1) % len(options)
        elif key == "\x1b[B":
            selected_idx = (selected_idx + 1) % len(options)
        elif key in ("\r", "\n"):
            return options[selected_idx][0]
        elif key == "\x03":
            raise KeyboardInterrupt

        # Move cursor back to the first option line to redraw the menu in place.
        print(f"\x1b[{len(options)}F", end="")


def _select_option(title: str, options: Sequence[tuple[str, str]]) -> str:
    """
    Arrow-key menu in interactive terminals.
    Fallback to numeric input for piped/non-interactive environments.
    """
    if sys.stdin.isatty() and sys.stdout.isatty():
        return _arrow_select_option(title, options)

    print(f"\n{title}")
    for idx, (_, label) in enumerate(options, 1):
        print(f"{idx}. {label}")

    valid_choices = {str(i) for i in range(1, len(options) + 1)}
    selected_idx = int(_prompt_choice("Choose an option: ", valid_choices)) - 1
    return options[selected_idx][0]


def _wind_menu(wind: Wind):
    while True:
        choice = _select_option(
            "Winding options",
            [
                ("wire0", "wind wire 0"),
                ("wire1", "wind wire 1"),
                ("wire2", "wind wire 2"),
                ("continuous", "continuous winding"),
                ("back", "back"),
            ],
        )
        if choice == "wire0":
            sleep(0.1)
            wind.wind(0)
            wind.move_motor(0, wind.m0_zero)
        elif choice == "wire1":
            sleep(0.1)
            wind.wind(1)
            wind.move_motor(0, wind.m0_zero)
        elif choice == "wire2":
            sleep(0.1)
            wind.wind(2)
            wind.move_motor(0, wind.m0_zero)
        elif choice == "continuous":
            wind.continuous_winding()
        else:
            return


def _motor_position_menu(wind: Wind):
    while True:
        choice = _select_option(
            "Motor position options",
            [
                ("get", "Get motors positions"),
                ("init", "Initialize the motor positions"),
                ("zero", "move the all motor position to zero"),
                ("back", "back"),
            ],
        )
        if choice == "get":
            positions = {
                "M0": wind.get_motor_position(0),
                "M1": wind.get_motor_position(1),
                "M2": wind.get_motor_position(2),
                "M3": wind.get_motor_position(3),
            }
            print(positions)
        elif choice == "init":
            wind.init_position()
        elif choice == "zero":
            wind.back_to_zero()
        else:
            return


def main(wind: Wind):
    while True:
        choice = _select_option(
            "Choose an option",
            [
                ("wind", "wind wires"),
                ("motor", "adjust motor positions"),
                ("close", "close the process"),
            ],
        )
        if choice == "wind":
            _wind_menu(wind)
        elif choice == "motor":
            _motor_position_menu(wind)
        else:
            return


if __name__ == "__main__":
    simulation = "--simulation" in sys.argv or "-s" in sys.argv
    config_file = "settings.yml"
    if simulation:
        config_file = "tests/dev-24n22p-settings.yml"
    wind = Wind(config_file, simulation)
    try:
        main(wind)
    except KeyboardInterrupt:
        if not simulation:
            wind.estop()
        print("Keyboard interrupt detected. Exiting...")
    finally:
        wind.close()
    exit()
