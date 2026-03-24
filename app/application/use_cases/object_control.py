from app.domain.services.api_client_port import VehicleApiClientPort


class ObjectControlUseCase:
    def __init__(self, api_client: VehicleApiClientPort):
        self.api_client = api_client

    async def get_position(self, object_id: int):
        return await self.api_client.get_object_position(object_id)

    async def move(self, object_id: int, x: int):
        return await self.api_client.move_object(object_id, x)
