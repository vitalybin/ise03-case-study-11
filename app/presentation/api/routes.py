from __future__ import annotations

from fastapi import APIRouter, Depends

from app.application.dto.control_requests import (
    ObjectMoveRequest,
    RawSteerRequest,
    RawThrottleRequest,
    StepMoveRequest,
)
from app.application.use_cases.get_lidar_data import GetLidarDataUseCase
from app.application.use_cases.get_status import GetStatusUseCase
from app.application.use_cases.object_control import ObjectControlUseCase
from app.application.use_cases.raw_control import RawControlUseCase
from app.application.use_cases.reset_vehicle import ResetVehicleUseCase
from app.application.use_cases.step_move_vehicle import StepMoveVehicleUseCase
from app.domain.entities.vehicle import Direction
from app.container import get_container

router = APIRouter(prefix='/api', tags=['vehicle-control'])


def get_status_uc() -> GetStatusUseCase:
    return get_container().get_status_use_case()


def get_lidar_uc() -> GetLidarDataUseCase:
    return get_container().get_lidar_use_case()


def get_reset_uc() -> ResetVehicleUseCase:
    return get_container().get_reset_use_case()


def get_raw_control_uc() -> RawControlUseCase:
    return get_container().get_raw_control_use_case()


def get_object_uc() -> ObjectControlUseCase:
    return get_container().get_object_control_use_case()


def get_step_move_uc() -> StepMoveVehicleUseCase:
    return get_container().get_step_move_use_case()


@router.get('/status')
async def status(uc: GetStatusUseCase = Depends(get_status_uc)):
    return await uc.execute()


@router.get('/lidar')
async def lidar(uc: GetLidarDataUseCase = Depends(get_lidar_uc)):
    return await uc.execute()


@router.post('/reset')
async def reset(uc: ResetVehicleUseCase = Depends(get_reset_uc)):
    return await uc.execute()


@router.post('/steer')
async def steer(request: RawSteerRequest, uc: RawControlUseCase = Depends(get_raw_control_uc)):
    return await uc.steer(request.value)


@router.post('/throttle')
async def throttle(request: RawThrottleRequest, uc: RawControlUseCase = Depends(get_raw_control_uc)):
    return await uc.throttle(request.value)


@router.post('/move/{direction}')
async def move(direction: Direction, request: StepMoveRequest, uc: StepMoveVehicleUseCase = Depends(get_step_move_uc)):
    result = await uc.execute(direction=direction, step_percent=request.step_percent, duration_ms=request.duration_ms)
    return {'direction': direction, 'planExecution': result}


@router.get('/object/{object_id}')
async def get_object(object_id: int, uc: ObjectControlUseCase = Depends(get_object_uc)):
    return await uc.get_position(object_id)


@router.post('/object/move')
async def move_object(request: ObjectMoveRequest, uc: ObjectControlUseCase = Depends(get_object_uc)):
    return await uc.move(object_id=request.object_id, x=request.x)


@router.get('/capabilities')
async def capabilities():
    return {
        'documentedCapabilities': [
            {
                'name': 'Status abfragen',
                'method': 'GET',
                'path': '/status',
                'uiSupport': 'Status-Panel mit Rohdatenansicht',
            },
            {
                'name': 'Lidar-Daten abfragen',
                'method': 'GET',
                'path': '/lidardata',
                'uiSupport': 'Lidar-Panel mit Rohdatenansicht',
            },
            {
                'name': 'Reset',
                'method': 'POST',
                'path': '/reset',
                'uiSupport': 'Reset-Button',
            },
            {
                'name': 'Lenkung',
                'method': 'POST',
                'path': '/steer/{value}',
                'valueRange': '-100..100 (aus Dokumentation ableitbar: Prozentwerte)',
                'uiSupport': 'Slider + Schnellbuttons',
            },
            {
                'name': 'Throttle/Gas',
                'method': 'POST',
                'path': '/throttle/{value}',
                'valueRange': '-100..100 inkl. Stop bei 0',
                'uiSupport': 'Slider + Schnellbuttons + Stop',
            },
            {
                'name': 'Karton verschieben',
                'method': 'POST',
                'path': '/object?id={id}&x={x}',
                'uiSupport': 'Objekt-Formular',
            },
            {
                'name': 'Kartonposition lesen',
                'method': 'GET',
                'path': '/object?id={id}',
                'uiSupport': 'Objekt-Panel',
            },
        ],
        'derivedCapabilities': [
            'Schrittbewegung vorwärts/rückwärts über zeitgesteuertes Throttle + Stop',
            'Schrittbewegung links/rechts über kombinierte Lenk- und Throttle-Kommandos',
            'Feinsteuerung über freie Prozentwerte für Throttle und Steering',
            'Not-Stopp über Throttle 0',
            'Manuelle Testoberfläche zum Explorieren aller dokumentierten Endpunkte',
        ],
        'limitations': [
            'Die API dokumentiert keine direkte Distanz- oder Winkelrückmeldung pro Fahrkommando.',
            'Schritte sind daher zeitbasiert und nur approximativ reproduzierbar.',
            'Weitere Sensorik außer Front-Lidar ist in der gelieferten Doku nicht dokumentiert.',
        ],
    }
