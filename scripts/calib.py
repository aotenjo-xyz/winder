import serial
from time import sleep
from winding import Wind

from utils import init_logger, load_config

# Load configuration
config = load_config()
PORT = config["serial"]["port"]
BAUDRATE = config["serial"]["baudrate"]

ser = serial.Serial(PORT, BAUDRATE)
logger = init_logger()


def main():
    wind = Wind()
    while True:
        key = input().strip()
        motor_id = key[0]
        target = key[1:]

        if key == "q":
            break
        if key == "e":
            wind.estop()
            break
        else:
            sleep(0.1)
            wind.move_motor(int(motor_id), float(target))
            sleep(0.1)

    ser.close()

    logger.info("Done")
    exit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
        ser.close()
        exit()
