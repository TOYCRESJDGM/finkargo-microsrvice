from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PositionSchema(BaseModel):
    positionName: str
    entityId: int
    creationDate: Optional[datetime]
    ModificationDate: Optional[datetime]
    deleted: Optional[bool] = False

class PositionCreate(PositionSchema):
    pass

class PositionUpdate(PositionSchema):
    positionName: Optional[str]
    entityId: Optional[int]

class Position(PositionSchema):
    position_id: int = None

    class Config:
        orm_mode = True