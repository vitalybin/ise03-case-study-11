from __future__ import annotations

import asyncio
from typing import Any

from app.domain.entities.vehicle import Direction
from app.domain.services.api_client_port import VehicleApiClientPort
from app.domain.services.movement_planner import MovementPlanner


class StepMoveVehicleUseCase:
    def __init__(self, api_client: VehicleApiClientPort, movement_planner: MovementPlanner):
        self.api_client = api_client
        self.movement_planner = movement_planner

    async def execute(self, direction: Direction, step_percent: int, duration_ms: int) -> list[dict[str, Any]]:
        plan = self.movement_planner.plan(direction=direction, step_percent=step_percent, duration_ms=duration_ms)
        results: list[dict[str, Any]] = []

        for idx, item in enumerate(plan, start=1):
            steer_result = await self.api_client.steer(item.steer)
            throttle_result = await self.api_client.throttle(item.throttle)
            results.append(
                {
                    'step': idx,
                    'command': {
                        'steer': item.steer,
                        'throttle': item.throttle,
                        'duration_ms': item.duration_ms,
                    },
                    'apiResponses': {
                        'steer': steer_result,
                        'throttle': throttle_result,
                    },
                }
            )
            if item.duration_ms > 0:
                await asyncio.sleep(item.duration_ms / 1000)

        return results
