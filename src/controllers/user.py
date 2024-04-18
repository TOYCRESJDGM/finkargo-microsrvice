from typing import Any
from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.controllers.base import BaseController
import src.models as models
import src.schemas as schemas
from src.utils import Singleton
import src.utils.encrypt as crypto
from src.utils.settings import ( JWT_KEY) 

"""
This class is a CRUD class for the user table.
"""

class UserCRUD(
    
    BaseController[schemas.User, schemas.UserCreate, schemas.UserUpdate],
    metaclass=Singleton,
):
    def __init__(self):
        super().__init__(models.User)
    
    def get_by_email(self, db: Session ,email: Any):
        return db.query(self.model_cls).filter(self.model_cls.email == email, self.model_cls.deleted == False).first()
    
    def login_user(self, db: Session, auth: Any):
        user = UserCRUD.get_by_email(self, db, auth.email)
        if user:
            decryptpassword = crypto.decrypt_password(user.password)
            if decryptpassword == auth.password:

                access = crypto.create_acces_token(user.id, user.userName, timedelta(minutes=60))
                
                return {
                    "type": "sucess",
                    "message": "Bienvenido/a {}".format(user.userName),
                    "data":{
                        "type": 'Bearer',
                        "token": access,
                        "user":{
                            "name": user.userName,
                            "id": user.id,
                            "email": user.email,
                            "phone": user.phone
                        }
                    }
                }
            else:
                raise HTTPException(status_code=401, detail="Could not validate user")
        else:
            raise HTTPException(status_code=401, detail="Could not validate user")

# Create a singleton instance of the UserCRUD class
user = UserCRUD()