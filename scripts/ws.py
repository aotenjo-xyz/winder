import asyncio
import websockets
import json
from utils import load_config
from db import get_all_motors
from datetime import datetime
import sqlite3

config = load_config()
fps = 60
frame_duration = 1 / fps
# logger = init_logger()

motor_velocities = [
    config['motor']['M0']['velocity'],
    config['motor']['M1']['velocity'],
    config['motor']['M2']['velocity'],
    config['motor']['M3']['velocity'],
]

def calculate_motor_position(motor_id, all_motors):
    velocity = motor_velocities[motor_id]
    target = all_motors[motor_id][1]
    position = all_motors[motor_id][2]
    timestamp = all_motors[motor_id][3]
    time_diff = (datetime.now() - datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')).total_seconds()
    if abs(target - position) < 0.01:
        return round(target, 3)
    estimated_position = position + (velocity * time_diff if target > position else -velocity * time_diff)
    if (target > position and estimated_position > target) or (target < position and estimated_position < target):
        estimated_position = target
    return round(estimated_position, 3)


async def handler(websocket):
    conn = sqlite3.connect("motors.db")
    while True:
        all_motors = get_all_motors(conn)
        motor_positions = {
            "M0": calculate_motor_position(0, all_motors),
            "M1": calculate_motor_position(1, all_motors),
            "M2": calculate_motor_position(2, all_motors),
            "M3": calculate_motor_position(3, all_motors)
        }
        await websocket.send(json.dumps(motor_positions))
        await asyncio.sleep(frame_duration)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()

asyncio.run(main())
