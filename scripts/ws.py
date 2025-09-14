import asyncio
import websockets
import json
from src.utils import load_config
from src.db import get_all_motors
from datetime import datetime
import sqlite3
import math

config_file = "settings.yml"
config = load_config(config_file)
fps = 60
frame_duration = 1 / fps
# logger = init_logger()

motor_velocities = [
    config["motor"]["M0"]["velocity"],
    config["motor"]["M1"]["velocity"],
    config["motor"]["M2"]["velocity"],
    config["motor"]["M3"]["velocity"],
]

m1_zero = config["motor"]["M1"]["zero"]
slot_count = config["winding"]["slot_count"]

def calculate_motor_position(motor_id, all_motors):
    velocity = motor_velocities[motor_id]
    target = all_motors[motor_id][1]
    position = all_motors[motor_id][2]
    timestamp = all_motors[motor_id][3]
    time_diff = (
        datetime.now() - datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    ).total_seconds()
    if abs(target - position) < 0.01:
        return round(target, 3)
    estimated_position = position + (
        velocity * time_diff if target > position else -velocity * time_diff
    )
    if (target > position and estimated_position > target) or (
        target < position and estimated_position < target
    ):
        estimated_position = target
    return round(estimated_position, 3)

def get_current_slot(motor1_pos):
    diff = abs(m1_zero - motor1_pos)
    slot_number = int(round(diff / ((math.pi * 2) / slot_count)))
    if slot_number >= slot_count:
        return slot_number % slot_count  
    return slot_number

async def handler(websocket):
    data_path = "data/motors.db"
    conn = sqlite3.connect(data_path)
    while True:
        all_motors = get_all_motors(conn)
        motor1_pos = calculate_motor_position(1, all_motors)
        current_slot = get_current_slot(motor1_pos)
        motor_positions = {
            "M0": calculate_motor_position(0, all_motors),
            "M1": motor1_pos,
            "M2": calculate_motor_position(2, all_motors),
            "M3": calculate_motor_position(3, all_motors),
            "slot": current_slot,
        }
        await websocket.send(json.dumps(motor_positions))
        await asyncio.sleep(frame_duration)


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
        exit()
