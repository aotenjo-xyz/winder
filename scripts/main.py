from src.winding import Wind
from time import sleep
import sys


def _prompt_choice(prompt: str, valid_choices: set[str]) -> str:
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"Invalid choice: {choice}. Please choose one of {sorted(valid_choices)}")


def _wind_menu(wind: Wind):
    while True:
        print("\nWinding options:")
        print("1. wind wire 0")
        print("2. wind wire 1")
        print("3. wind wire 2")
        print("4. continuous winding")
        print("5. back")

        choice = _prompt_choice("Choose an option: ", {"1", "2", "3", "4", "5"})
        if choice == "1":
            sleep(0.1)
            wind.wind(0)
            wind.move_motor(0, wind.m0_zero)
        elif choice == "2":
            sleep(0.1)
            wind.wind(1)
            wind.move_motor(0, wind.m0_zero)
        elif choice == "3":
            sleep(0.1)
            wind.wind(2)
            wind.move_motor(0, wind.m0_zero)
        elif choice == "4":
            wind.continuous_winding()
        else:
            return


def _motor_position_menu(wind: Wind):
    while True:
        print("\nMotor position options:")
        print("1. Get motors positions")
        print("2. Initialize the motor positions")
        print("3. move the all motor position to zero")
        print("4. back")

        choice = _prompt_choice("Choose an option: ", {"1", "2", "3", "4"})
        if choice == "1":
            positions = {
                "M0": wind.get_motor_position(0),
                "M1": wind.get_motor_position(1),
                "M2": wind.get_motor_position(2),
                "M3": wind.get_motor_position(3),
            }
            print(positions)
        elif choice == "2":
            wind.init_position()
        elif choice == "3":
            wind.back_to_zero()
        else:
            return


def main(wind: Wind):
    while True:
        print("\nChoose an option:")
        print("1. wind wires")
        print("2. adjust motor positions")
        print("3. close the process")

        choice = _prompt_choice("Choose an option: ", {"1", "2", "3"})
        if choice == "1":
            _wind_menu(wind)
        elif choice == "2":
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
