from __future__ import annotations

import os

from app.application.use_cases.get_lidar_data import GetLidarDataUseCase
from app.application.use_cases.get_status import GetStatusUseCase
from app.application.use_cases.object_control import ObjectControlUseCase
from app.application.use_cases.raw_control import RawControlUseCase
from app.application.use_cases.reset_vehicle import ResetVehicleUseCase
from app.application.use_cases.step_move_vehicle import StepMoveVehicleUseCase
from app.domain.services.movement_planner import MovementPlanner
from app.infrastructure.gateways.interacting_systems_api_client import InteractingSystemsApiClient


class Container:
    def __init__(self) -> None:
        base_url = os.getenv('VEHICLE_API_BASE_URL', 'https://www.interagierende-systeme.de:8000')
        self.api_client = InteractingSystemsApiClient(base_url=base_url)
        self.movement_planner = MovementPlanner()

    def get_status_use_case(self) -> GetStatusUseCase:
        return GetStatusUseCase(self.api_client)

    def get_lidar_use_case(self) -> GetLidarDataUseCase:
        return GetLidarDataUseCase(self.api_client)

    def get_reset_use_case(self) -> ResetVehicleUseCase:
        return ResetVehicleUseCase(self.api_client)

    def get_raw_control_use_case(self) -> RawControlUseCase:
        return RawControlUseCase(self.api_client)

    def get_object_control_use_case(self) -> ObjectControlUseCase:
        return ObjectControlUseCase(self.api_client)

    def get_step_move_use_case(self) -> StepMoveVehicleUseCase:
        return StepMoveVehicleUseCase(self.api_client, self.movement_planner)


container: Container | None = None


def get_container() -> Container:
    assert container is not None
    return container
