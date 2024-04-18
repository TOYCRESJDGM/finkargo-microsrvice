from fastapi import Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from src.adapters.mysql_adapter import get_db
import src.controllers as controller
import src.schemas as schemas
import src.utils.encrypt as crypto

router = InferringRouter()

@cbv(router)
class UserRouter:
    # dependency injection
    db: Session = Depends(get_db)

    @router.post("/register")
    def register_user(self, user:schemas.UserCreate) -> dict:
        """
        register and create a user
        :return:
        """
        try:
            user.password = crypto.encrypt_password(user.password)
            controller.user.create(self.db, entity=user)
            return {
                "type": "sucess",
                "message": "user create successfull",
                "data": []
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    
    @router.post("/login")
    def auth_user(self, auth: schemas.UserAuth) -> dict:
        """
        login a user
        :return:
        """
        user = controller.user.get_by_email(self.db, auth.email)
        if user:
            response = controller.user.login_user(self.db, auth)
        else:
            response = {
                "type": "error",
                "message": "credentials error",
                "data": []
            }
            
        return response
