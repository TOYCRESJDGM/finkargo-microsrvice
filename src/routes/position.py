from fastapi import Depends, HTTPException,  APIRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from typing import Optional, Annotated, Dict, Any

from src.utils.encrypt import get_current_user

from src.adapters.mysql_adapter import get_db
from src.utils.logger import logger
from src.utils.mappers import mapper_position
import src.controllers as controller
import src.schemas as schemas

router = APIRouter()



@cbv(router)
class PositionRouter:
    # dependency injection
    db: Session = Depends(get_db)

    user_dependency = Annotated[dict, Depends(get_current_user)]

    @router.post("/create")
    def create_position(self, user: user_dependency, position:schemas.PositionCreate) -> Dict[str, Any]:
        """
        create a position
        :return:
        """
        if user is None:
            raise HTTPException(status_code=401, detail='Autenticated neded')
        try:
            logger.info("position creation process started")
            controller.position.create(self.db, entity=position)
            return {
                "type": "sucess",
                "message": "position create successfull",
                "data": []
            }
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=400, detail=str(e))


    @router.get("/")
    def get_positions(self, user: user_dependency, entity_id: Optional[int] = None, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get all positions
        :return:
        """
        if user is None:
            raise HTTPException(status_code=401, detail='Autenticated neded')
        
        logger.info("get positions process started")

        positions = controller.position.search_position(self.db, entity_id, name)
        
        if not positions:
            logger.info("position not found")
            raise HTTPException(status_code=404, detail="position not found")
        
        logger.info("successfully completed process")
            
        return {
                "type": "success",
                "message": "successfully completed process",
                "data": list(map(mapper_position, positions)),
                "total": len(positions)
        }
        

    @router.get("/{id}")
    def get_position(self, user: user_dependency, id:int) -> Dict[str, Any]:
        """
        Get a single position
        :return:
        """
        if user is None:
            raise HTTPException(status_code=401, detail='Autenticated neded')
        
        logger.info("get position process started")
        position =  controller.position.get_with_entity(self.db, id)
        
        if not position:
            logger.info("position not found")
            raise HTTPException(status_code=404, detail="position not found")
        
        logger.info("successfully completed process")
            
        return {
                "type": "sucess",
                "message": "successfully completed process",
                "data": mapper_position(position)
            }
    
    @router.put("/{id}")
    def update_position(self, user: user_dependency, id: int, info: schemas.PositionUpdate) -> Dict[str, Any]:
        """
        Update a position
        :return:
        """
        if user is None:
            raise HTTPException(status_code=401, detail='Autenticated neded')
        
        logger.info("update position process started")

        try:
            position = controller.position.get(self.db, id)
            if not position:
                logger.info("position not found")
                raise HTTPException(status_code=404, detail="position not found")
            update_position = controller.position.update(self.db, model_id=id, entity=info)
            logger.info("successfully completed process")
            return {
                "type": "success",
                "message": "successfully completed process",
                "data": mapper_position(update_position)
            }
        except HTTPException as http_error:
            raise http_error
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise HTTPException(status_code=500, detail="An error occurred while updating the position")
    
    @router.put("/delete/{id}")
    def soft_delete_position(self, user: user_dependency, id: int, info: schemas.PositionUpdate):
        """
        Soft delete an position by setting the 'deleted' flag to True.
        """

        if user is None:
            raise HTTPException(status_code=401, detail='Autenticated neded')
        
        logger.info("delete position process started")

        try:

            position = controller.position.get(self.db, id)
            if not position:
                logger.info("position not found")
                raise HTTPException(status_code=404, detail="position not found")

            controller.position.soft_delete(self.db, model_id=id, entity=info)

            logger.info("position deleted successfully")

            return {
                "type": "sucess",
                "message": "position deleted successfully",
                "data": []
            }
        
        except HTTPException as http_error:
            raise http_error
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise HTTPException(status_code=500, detail="An error occurred while deleting the position")