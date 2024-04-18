from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserSchema(BaseModel):
    userName: str
    email: str
    phone: str
    password: str
    creationDate: Optional[datetime]
    ModificationDate: Optional[datetime]
    deleted: Optional[bool] = False

class UserCreate(UserSchema):
    pass

class UserUpdate(UserSchema):
    pass

class UserAuth(BaseModel):
    email: str 
    password: str

class User(UserSchema):
    user_id: int = None

    class Config:
        orm_mode = True