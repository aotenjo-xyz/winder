from pydantic import BaseModel, Field


class SerialConfig(BaseModel):
    port: str
    baudrate: int = Field(gt=0)

class LoggingConfig(BaseModel):
    level: str

class Motor0Config(BaseModel):
    direction: bool
    wind_range_end: float
    wind_range_start: float
    end_to_zero: float
    velocity: float = Field(gt=0)
    vP: float
    vI: float
    vD: float
    pP: float
    voltage_limit: float
    velocirty_limit: float
    lpfTf: float


class Motor1Config(BaseModel):
    direction: bool
    zero: float
    end_to_rotating_position: float
    velocity: float = Field(gt=0)
    vP: float
    vI: float
    vD: float
    pP: float
    voltage_limit: float
    velocirty_limit: float
    lpfTf: float


class Motor2Config(BaseModel):
    direction: bool
    zero: float
    angle_to_prevent_collision: float
    velocity: float = Field(gt=0)
    vP: float
    vI: float
    vD: float
    pP: float
    voltage_limit: float
    velocirty_limit: float
    lpfTf: float


class Motor3Config(BaseModel):
    direction: bool
    pull_wire_torque: float
    wind_torque: float
    velocity: float = Field(gt=0)


class MotorConfig(BaseModel):
    M0: Motor0Config
    M1: Motor1Config
    M2: Motor2Config
    M3: Motor3Config


class WindingConfig(BaseModel):
    turns: int = Field(gt=0)
    starts_at: int = Field(ge=0)
    winding_config: str
    dont_move_m3: bool = False


class MachineConfig(BaseModel):
    serial: SerialConfig
    logging: LoggingConfig
    motor: MotorConfig
    winding: WindingConfig
