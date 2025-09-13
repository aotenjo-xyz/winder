from winding import Wind
from time import sleep
import sys


def main(simulation=False):
    wind = Wind(simulation)
    # wind.back_to_zero()
    while True:
        key = input().strip()
        if key == "k":
            sleep(0.1)

            wind.wind(0)

        elif key == "j":
            sleep(0.1)

            wind.wind(1)

        elif key == "h":
            sleep(0.1)

            wind.wind(2)

        elif key == "g":
            wind.continuous_winding()

        elif key == "i":
            wind.init_position()

        elif key == "z":
            wind.back_to_zero()

        elif len(key) > 1 and key[0] == "s":
            slot = int(key[1:])
            wind.move_to_slot(slot)

        elif key == "e":
            wind.estop()
            break

        elif key == "t":
            m2_pos = wind.get_motor_position(2)
            print(m2_pos)
            break

        elif key == "b":
            m1_pos = wind.get_motor_position(1)
            print(m1_pos)
            break

        elif key == "l":
            ports = wind.available_ports()
            print(ports)
            break

        elif key == "q":
            wind.close()
            break
        else:
            break


if __name__ == "__main__":
    simulation = "--simulation" in sys.argv or "-s" in sys.argv
    try:
        main(simulation)
    except KeyboardInterrupt:
        wind = Wind(simulation)
        if not simulation:
            wind.estop()
            print("Keyboard interrupt detected. Exiting...")
        exit()
