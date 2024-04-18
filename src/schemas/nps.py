from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator

class NpsSchema(BaseModel):
    score: int
    positionId: int
    userId: Optional[int]
    creationDate: Optional[datetime]
    ModificationDate: Optional[datetime]
    deleted: Optional[bool] = False

    @validator('score')
    def score_limit(cls, v):
        if v < 0 or v > 10:
            raise ValueError('Score must be between 0 and 10')
        return v
    
class NpsCreate(NpsSchema):
    pass

class NpsUpdate(NpsSchema):
    pass

class Nps(NpsSchema):
    nps_id: int = None

    class Config:
        orm_mode = True
