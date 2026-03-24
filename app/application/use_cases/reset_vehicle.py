from app.domain.services.api_client_port import VehicleApiClientPort


class ResetVehicleUseCase:
    def __init__(self, api_client: VehicleApiClientPort):
        self.api_client = api_client

    async def execute(self):
        return await self.api_client.reset()
