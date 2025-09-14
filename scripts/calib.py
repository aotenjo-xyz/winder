from time import sleep
from src.winding import Wind

def main():
    config_file = "settings.yml"
    wind = Wind(config_file)
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

    wind.close()
    exit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
        exit()
