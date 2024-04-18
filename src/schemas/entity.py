from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class EntitySchema(BaseModel):
    entityName: str
    locationId: int
    type: str
    creationDate: Optional[datetime]
    ModificationDate: Optional[datetime]
    deleted: Optional[bool] = False

class EntityCreate(EntitySchema):
    pass

class EntityUpdate(EntitySchema):
    entityName: Optional[str]
    locationId: Optional[int]
    type: Optional[str]

class EntitySoftDelete(EntitySchema):
    entityName: Optional[str]
    locationId: Optional[int]
    type: Optional[str]

class Entity(EntitySchema):
    Entity_id: int = None

    class Config:
        orm_mode = True