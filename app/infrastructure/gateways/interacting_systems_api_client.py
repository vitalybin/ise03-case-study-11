from __future__ import annotations

import httpx
from typing import Any

from app.domain.services.api_client_port import VehicleApiClientPort


class InteractingSystemsApiClient(VehicleApiClientPort):
    def __init__(self, base_url: str, timeout_seconds: float = 10.0):
        self._base_url = base_url.rstrip('/')
        self._client = httpx.AsyncClient(base_url=self._base_url, timeout=timeout_seconds, verify=True)

    async def close(self) -> None:
        await self._client.aclose()

    async def _handle(self, response: httpx.Response) -> Any:
        response.raise_for_status()
        content_type = response.headers.get('content-type', '')
        if 'application/json' in content_type:
            return response.json()
        try:
            return response.json()
        except Exception:
            return {'raw': response.text}

    async def get_status(self) -> Any:
        return await self._handle(await self._client.get('/status'))

    async def get_lidar_data(self) -> Any:
        return await self._handle(await self._client.get('/lidardata'))

    async def reset(self) -> Any:
        return await self._handle(await self._client.post('/reset'))

    async def steer(self, value: int) -> Any:
        return await self._handle(await self._client.post(f'/steer/{value}'))

    async def throttle(self, value: int) -> Any:
        return await self._handle(await self._client.post(f'/throttle/{value}'))

    async def get_object_position(self, object_id: int) -> Any:
        return await self._handle(await self._client.get('/object', params={'id': object_id}))

    async def move_object(self, object_id: int, x: int) -> Any:
        return await self._handle(await self._client.post('/object', params={'id': object_id, 'x': x}))
