from pydantic import BaseModel, Field


class StepMoveRequest(BaseModel):
    step_percent: int = Field(default=18, ge=1, le=100)
    duration_ms: int = Field(default=450, ge=100, le=5000)


class RawSteerRequest(BaseModel):
    value: int = Field(ge=-100, le=100)


class RawThrottleRequest(BaseModel):
    value: int = Field(ge=-100, le=100)


class ObjectMoveRequest(BaseModel):
    object_id: int = Field(default=4, alias='objectId')
    x: int

    model_config = {
        'populate_by_name': True
    }
