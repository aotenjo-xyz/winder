import serial
from time import sleep
import math
from config import wind_orders, slot_indices, rotating_directions, m2_gear_ratio
from utils import init_logger, load_config
from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from db import update_motor_position, update_motor_target, init_db


class Motor2State(Enum):
    TOP = 0
    BOTTOM = 1
    TOP_LEFT = 2
    TOP_RIGHT = 3
    BOTTOM_LEFT = 4
    BOTTOM_RIGHT = 5

    def __str__(self):
        return self.name

class MotorPosition(BaseModel):
    motor_id: int
    position: float
    timestamp: datetime


class Wind:

    def __init__(self, simulation=False):
        self.motor_positions = [0, 0, 0, 0]
        self.motor2_pos = Motor2State.TOP
        self.config = load_config()
        baudrate = self.config["serial"]["baudrate"]
        port = self.config["serial"]["port"]
        self.simulation = simulation
        self.motor_velocities = [
            self.config['motor']['M0']['velocity'],
            self.config['motor']['M1']['velocity'],
            self.config['motor']['M2']['velocity'],
            self.config['motor']['M3']['velocity'],
        ]
        self.motor_positions_in_simulation = [
            MotorPosition(motor_id=i, position=0.0, timestamp=datetime.now())
            for i in range(4)
        ]
        if not simulation:
            port = self.config['serial']['port']
            self.ser = serial.Serial(port, baudrate)
        else:
            self.conn = init_db()

        self.logger = init_logger()

        self.turns_per_slot = self.config["winding"]["turns_per_slot"]
        self.slot_pairs = self.config["winding"]["slot_pairs"]

        self.m0_wind_range = (
            self.config["motor"]["M0"]["wind_range_start"],
            self.config["motor"]["M0"]["wind_range_end"],
        )
        self.m0_zero = self.config["motor"]["M0"]["end_to_zero"] + self.m0_wind_range[1]
        self.m1_zero = self.config["motor"]["M1"]["zero"]
        self.m2_zero = self.config["motor"]["M2"]["zero"]

        self.starts_at = self.config["winding"]["starts_at"]

        self.m1_rotating_position = (
            self.config["motor"]["M1"]["end_to_rotating_position"]
            + self.m0_wind_range[1]
        )
        self.m2_angle_to_prevent_collision = self.config["motor"]["M2"][
            "angle_to_prevent_collision"
        ]

        if self.config["winding"]["dont_move_m3"]:
            self.m3_wind_torque = 0
            self.m3_slow_wind_torque = 0
            self.m3_pull_wire_torque = 0
        else:
            self.m3_wind_torque = self.config["motor"]["M3"]["wind_torque"]
            self.m3_slow_wind_torque = 0.03
            self.m3_pull_wire_torque = self.config["motor"]["M3"]["pull_wire_torque"]

    def calculate_motor_position_in_simulation(self, motor_id):
        target_position = self.motor_positions[motor_id]
        velocity = self.motor_velocities[motor_id]
        motor_position_in_simulation = self.motor_positions_in_simulation[motor_id]
        time_diff = (datetime.now() - motor_position_in_simulation.timestamp).total_seconds()
        position_diff = target_position - motor_position_in_simulation.position
        if abs(position_diff) < 0.01:
            return target_position
        max_movement = velocity * time_diff
        if abs(position_diff) <= max_movement:
            return target_position
        return motor_position_in_simulation.position + (max_movement if position_diff > 0 else -max_movement)


    def check_motor_direction(self, motor_id, target):
        rotating_direction = rotating_directions[motor_id]
        if not rotating_direction:
            return -target
        return target

    def adjust_motor_position_from_gear_ratio(self, target, gear_ratio, inverse=False):
        if inverse:
            return target / gear_ratio
        return target * gear_ratio

    def move_motor(self, motor_id, target, round_to=3):
        motor_target = self.check_motor_direction(motor_id, target)
        if motor_id == 2:
            motor_target = self.adjust_motor_position_from_gear_ratio(
                motor_target, m2_gear_ratio
            )

        motor_target = round(motor_target, round_to)
        command = f"M{motor_id}A{motor_target}\n"

        self.motor_positions[motor_id] = target

        if self.simulation:
            self.motor_positions_in_simulation[motor_id] = MotorPosition(
                motor_id=motor_id,
                position=self.calculate_motor_position_in_simulation(motor_id),
                timestamp=datetime.now()
            )
            self.logger.debug(f'Simulation mode: {command.strip()}')
            update_motor_target(self.conn, motor_id, target)
            if motor_id != 2 and motor_id != 3:
                # motor 3 is for wire tension, we don't care about its position
                motor_position_in_simulation = self.calculate_motor_position_in_simulation(motor_id)
                update_motor_position(self.conn, motor_id, motor_position_in_simulation)
            return
        self.ser.write(bytes(command, "utf-8"))
        self.logger.debug(command.strip())

    def init_position(self, pull_wire=False):
        """
        Move all motors to zero position
        """
        self.move_motor(1, self.m1_zero)
        self.move_motor(0, self.m0_zero)
        self.move_motor(2, self.m2_zero)

        sleep(0.5)
        if pull_wire:
            self.set_wire_tension(1)

    def set_wire_tension(self, wait_time=0.5):
        # pull the wire
        self.move_motor(3, self.m3_pull_wire_torque)
        sleep(wait_time)
        self.move_motor(3, self.m3_wind_torque)

    def estop(self):
        """
        Stop all motors
        """
        self.ser.write(b"ESTOP\n")
        self.logger.info("ESTOP")

    def back_to_zero(self):
        """
        Move all motors to absolute zero position
        """
        self.move_motor(0, 0)
        self.move_motor(1, 0)
        self.move_motor(2, 0)

        sleep(0.5)

    def available_ports(self):
        import serial.tools.list_ports

        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def get_motor_position(self, motor_id):
        if self.simulation:
            motor_position_in_simulation = self.calculate_motor_position_in_simulation(motor_id)
            update_motor_position(self.conn, motor_id, motor_position_in_simulation)
            return motor_position_in_simulation
        # Run M<motor_id>P to get the current position of the motor
        retries = 3
        while retries > 0:
            try:
                self.ser.write(bytes(f"M{motor_id}P\n", "utf-8"))
                break
            except serial.SerialException:
                retries -= 1
                self.logger.exception(f"SerialException: Retrying... ({3 - retries}/3)")
                sleep(1)
        else:
            raise serial.SerialException(
                "Failed to write to serial port after 3 retries"
            )

        # Read the response
        # Response format: M<motor_id>P<position>
        while True:
            if self.ser.in_waiting:
                line = self.ser.readline().decode("utf-8").rstrip()
                if len(line) > 2 and line[:3] == f"M{motor_id}P":
                    break
        motor_position = float(line.split("P")[1])
        motor_position = self.check_motor_direction(motor_id, motor_position)
        if motor_id == 2:
            motor_position = self.adjust_motor_position_from_gear_ratio(
                motor_position, m2_gear_ratio, True
            )
        return motor_position

    def move_to_slot(self, slot_idx: int):
        # k = 0.9958
        k = 1
        # winding counter-clockwise
        direction = -1
        self.move_motor(
            1, self.m1_zero + direction * (math.pi / self.slot_pairs) * slot_idx * k
        )

    def is_motor2_at_12oclock(self, _motor2_pos=None):
        # if motor2 is at 12 o'clock, self.motor_positions[2] - self.m2_zero == math.pi * 2 * n
        # if motor2 is at 6 o'clock, self.motor_positions[2] - self.m2_zero == math.pi * 2 * n + math.pi
        relative_pos = (
            self.motor_positions[2] - self.m2_zero
            if _motor2_pos is None
            else _motor2_pos - self.m2_zero
        )
        return (
            abs(relative_pos % (math.pi * 2)) < 0.1
            or abs(relative_pos % (math.pi * 2) - math.pi * 2) < 0.1
        )

    def is_motor2_should_be_at_12oclock(self, wind_idx):
        """
        For 24n22p motor, self.wind_slot_count = 8
        At wind_idx = 3, 7, motor2 should be at 12 o'clock
        """
        wind_indices = [int(self.wind_slot_count / 2 - 1), self.wind_slot_count - 1]
        return wind_idx in wind_indices

    def is_motor2_at_top(self):
        if (
            self.motor2_pos == Motor2State.TOP
            or self.motor2_pos == Motor2State.TOP_LEFT
            or self.motor2_pos == Motor2State.TOP_RIGHT
        ):
            return True
        return False

    def get_target_motor2_pos(self, clockwise, wind_idx):
        """
        When you rotate motor2 from 12 o'clock to 12 o'clock clockwise, the wire will be at the left position.
        To move the wire to the right position, you need to rotate motor2 by 180 degrees.
        """
        motor2_at_12oclock = self.is_motor2_at_top()
        # motor2_at_12oclock = self.is_motor2_at_12oclock()
        target_motor2_pos = self.motor_positions[
            2
        ] + math.pi * 2 * self.turns_per_slot * (1 if clockwise else -1)
        if self.motor2_pos == Motor2State.TOP_RIGHT:
            target_motor2_pos = (
                target_motor2_pos - self.m2_angle_to_prevent_collision
            )  # move to TOP position
            self.motor2_pos = Motor2State.TOP
        elif self.motor2_pos == Motor2State.BOTTOM_RIGHT:
            target_motor2_pos = target_motor2_pos + self.m2_angle_to_prevent_collision
            self.motor2_pos = Motor2State.BOTTOM

        # motor2 should be at 12 o'clock after winding the last slot
        if (
            motor2_at_12oclock
            and clockwise
            and not self.is_motor2_should_be_at_12oclock(wind_idx)
        ) or (not motor2_at_12oclock and not clockwise):
            # +/- 180 degrees
            target_motor2_pos = target_motor2_pos + math.pi * (1 if clockwise else -1)

        return target_motor2_pos

    def move_wire_to_right_position(self, slot_idx):
        # move to slot_idx - 1 and rotate motor2 by 180 degrees clockwise
        self.move_to_slot(slot_idx - 1)
        sleep(0.5)
        self.move_motor(0, self.m0_wind_range[0])
        sleep(1)
        if self.motor2_pos == Motor2State.TOP_LEFT:
            target_motor2_pos = (
                self.motor_positions[2] + math.pi + self.m2_angle_to_prevent_collision
            )
            self.move_motor(2, target_motor2_pos)
        else:
            self.logger.warning("motor2_pos is not TOP_LEFT")
            self.logger.warning(
                f"motor2_pos: {self.motor_positions[2]}, self.motor2_pos: {self.motor2_pos}"
            )
            raise Exception("motor2_pos is not TOP_LEFT")
        self.motor2_pos = Motor2State.BOTTOM

        sleep(0.3)

        motor2_pos = self.get_motor_position(2)
        assert (
            abs(motor2_pos - target_motor2_pos) < 0.1
        ), f"motor2_pos: {motor2_pos}, target_motor2_pos: {target_motor2_pos}"

        self.move_motor(0, self.m1_rotating_position)
        sleep(0.5)

    def set_motor2_wire_position(self):
        if self.motor2_pos == Motor2State.TOP_LEFT:
            self.move_motor(
                2, self.motor_positions[2] + self.m2_angle_to_prevent_collision * 2
            )
            self.motor2_pos = Motor2State.TOP_RIGHT
        elif self.motor2_pos == Motor2State.BOTTOM_LEFT:
            self.move_motor(
                2, self.motor_positions[2] - self.m2_angle_to_prevent_collision * 2
            )
            self.motor2_pos = Motor2State.BOTTOM_RIGHT
        elif self.motor2_pos == Motor2State.TOP:
            # initial position
            self.logger.debug("Motor2 is at top position")  # do nothing
        elif self.motor2_pos == Motor2State.BOTTOM:
            self.logger.debug("Motor2 is at bottom position")
            self.move_motor(
                2, self.motor_positions[2] - self.m2_angle_to_prevent_collision
            )
            self.motor2_pos = Motor2State.BOTTOM_RIGHT

    def get_motor0_target_winding_position(
        self, motor2_total_mileage, current_motor2_mileage
    ):
        wind_range_distance = abs(self.m0_wind_range[1] - self.m0_wind_range[0])
        target_motor0_mileage = (
            wind_range_distance * 2 / motor2_total_mileage * current_motor2_mileage
        )
        if target_motor0_mileage < wind_range_distance:
            motor0_target = self.m0_wind_range[0] + target_motor0_mileage
        else:
            motor0_target = self.m0_wind_range[1] - (
                target_motor0_mileage - wind_range_distance
            )
        assert (
            self.m0_wind_range[0] <= motor0_target <= self.m0_wind_range[1]
        ), f"motor0_target: {motor0_target} is out of range {self.m0_wind_range}"
        return motor0_target

    def prevent_collision(self):
        if self.is_motor2_at_12oclock():
            self.move_motor(
                2, self.motor_positions[2] - self.m2_angle_to_prevent_collision
            )
            self.motor2_pos = Motor2State.TOP_LEFT
        else:
            self.move_motor(
                2, self.motor_positions[2] + self.m2_angle_to_prevent_collision
            )
            self.motor2_pos = Motor2State.BOTTOM_LEFT

    def slow_winding(self, clockwise):
        rotating_count = 2
        steps_per_rotation = 30
        step = math.pi * 2 / steps_per_rotation * (1 if clockwise else -1)
        self.move_motor(3, self.m3_slow_wind_torque)
        for i in range(rotating_count * steps_per_rotation):
            self.move_motor(2, self.motor_positions[2] + step)
            sleep(0.1)
        self.move_motor(3, self.m3_wind_torque)

    def fast_winding(self, clockwise):
        rotating_count = 1
        steps_per_rotation = 12
        step = math.pi * 2 / steps_per_rotation * (1 if clockwise else -1)
        for i in range(rotating_count * steps_per_rotation):
            self.move_motor(2, self.motor_positions[2] + step)
            sleep(0.05)

    def wind_slot(self, slot_idx: int, clockwise, wind_idx):
        # rotate motor1
        if wind_idx == int(self.wind_slot_count / 2) and not clockwise:
            self.move_wire_to_right_position(slot_idx)

        self.move_to_slot(slot_idx)
        self.set_wire_tension()
        self.move_motor(0, self.m0_wind_range[1])
        sleep(0.3)
        self.set_motor2_wire_position()
        sleep(0.2)
        self.move_motor(0, self.m0_wind_range[0])
        sleep(0.7)

        init_motor2_pos = self.get_motor_position(2)
        assert (
            abs(init_motor2_pos - self.motor_positions[2]) < 0.1
        ), f"init_motor2_pos: {init_motor2_pos}, self.motor_positions[2]: {self.motor_positions[2]}"

        if self.motor2_pos == Motor2State.TOP_RIGHT:
            init_motor2_pos = init_motor2_pos - self.m2_angle_to_prevent_collision
        elif self.motor2_pos == Motor2State.BOTTOM_RIGHT:
            init_motor2_pos = init_motor2_pos + self.m2_angle_to_prevent_collision

        target_motor2_pos = self.get_target_motor2_pos(clockwise, wind_idx)
        # self.slow_winding(clockwise)
        self.fast_winding(clockwise)
        self.move_motor(2, target_motor2_pos)

        prev_motor2_pos = init_motor2_pos
        k = 1.0
        while True:
            motor2_pos = self.get_motor_position(2)
            sleep(0.03)
            if (
                abs(motor2_pos - prev_motor2_pos) >= math.pi * k - 0.01
            ):  # 0.01 is to avoid floating point error
                if not abs(motor2_pos - target_motor2_pos) < math.pi * 2:
                    target_motor0_pos = self.get_motor0_target_winding_position(
                        abs(target_motor2_pos - init_motor2_pos),
                        abs(motor2_pos - init_motor2_pos),
                    )
                    self.move_motor(0, target_motor0_pos)
                    prev_motor2_pos = motor2_pos
                    continue
                break

        sleep(0.3)
        motor2_pos = self.get_motor_position(2)
        assert (
            abs(motor2_pos - target_motor2_pos) < 0.1
        ), f"motor2_pos: {motor2_pos}, target_motor2_pos: {target_motor2_pos}"

        self.logger.info(f"Winding slot {slot_idx} done")

        # move motor 2 to the left to prevent collision
        skip_prevent_collision_slot_idx = [3, 11, 15, 19, 23]
        if slot_idx not in skip_prevent_collision_slot_idx:
            self.prevent_collision()
        sleep(0.3)

        self.move_motor(0, self.m1_rotating_position)
        sleep(0.7)

    def is_starting_from_bottom(self, starts_at: int, wire_idx: int):
        # when starting from 2, 5, 7 for wire A
        starts_at_from_bottom_a_c = [2, 5, 7]
        if wire_idx != 1 and starts_at in starts_at_from_bottom_a_c:
            return True

        # when starting from 1, 3 for wire B
        starts_at_from_bottom_b = [1, 3, 6]
        if wire_idx == 1 and starts_at in starts_at_from_bottom_b:
            return True
        return False

    def wind(self, wire_idx: int):
        wind_order = wind_orders[wire_idx]
        self.wind_slot_count = len(wind_orders[wire_idx])

        start_slot_idx = slot_indices[wire_idx][self.starts_at]
        self.move_to_slot(start_slot_idx)
        sleep(0.5)

        if self.is_starting_from_bottom(self.starts_at, wire_idx):
            # starting from the bottom
            self.move_motor(2, self.m2_zero + math.pi)
            sleep(15)

        for i in range(self.starts_at, int(self.slot_pairs * 2 / 3)):
            if self.starts_at == i and i != 0:
                self.prevent_collision()
                sleep(0.3)

                self.move_motor(0, self.m1_rotating_position)

            clockwise = wind_order[i]
            slot_idx = slot_indices[wire_idx][i]

            self.wind_slot(slot_idx, clockwise, i)

        if wire_idx != 2:
            self.wind_wire_around_shaft(wire_idx)
            self.motor2_pos = Motor2State.TOP

        # Back to zero
        self.move_motor(0, self.m0_zero)
        # self.move_motor(2, self.m2_zero)
        self.logger.info("Winding done")

    def wind_wire_around_shaft(self, wire_idx: int):
        # Move M1
        # start_slot_idx = slot_indices[wire_idx + 1][0]
        # self.move_to_slot(start_slot_idx)
        # sleep(0.5)

        motor1_pos = self.get_motor_position(1)

        # 2 full rotation of M1
        rotation_count = 2
        motor1_rotation = math.pi * 2 * rotation_count
        if wire_idx == 0:
            motor1_rotation = -motor1_rotation

        self.move_motor(1, motor1_pos + motor1_rotation)
        self.m1_zero += motor1_rotation
        sleep(1.5)

        motor2_pos = self.get_motor_position(2)
        self.m2_zero = motor2_pos

    def continuous_winding(self):
        self.init_position(True)

        self.wind(0)
        self.starts_at = 0
        self.wind(1)
        self.wind(2)

    def close(self):
        if not self.simulation:
            self.ser.close()
        else:
            self.conn.close()
            self.logger.info('Connection closed')
