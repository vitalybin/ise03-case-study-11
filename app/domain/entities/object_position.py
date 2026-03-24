from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ObjectPosition:
    raw: Any
