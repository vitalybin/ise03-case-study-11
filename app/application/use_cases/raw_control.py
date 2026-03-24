from app.domain.services.api_client_port import VehicleApiClientPort


class RawControlUseCase:
    def __init__(self, api_client: VehicleApiClientPort):
        self.api_client = api_client

    async def steer(self, value: int):
        return await self.api_client.steer(value)

    async def throttle(self, value: int):
        return await self.api_client.throttle(value)
