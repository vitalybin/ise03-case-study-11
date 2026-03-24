from dataclasses import dataclass
from enum import Enum


class Direction(str, Enum):
    FORWARD = 'forward'
    BACKWARD = 'backward'
    LEFT = 'left'
    RIGHT = 'right'


@dataclass(frozen=True)
class MovementStep:
    throttle: int
    steer: int
    duration_ms: int
