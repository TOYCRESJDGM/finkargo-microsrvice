from fastapi import Depends, HTTPException, APIRouter

from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from typing import Optional, Annotated, Dict, Any

from src.utils.encrypt import get_current_user

from src.adapters.mysql_adapter import get_db
from src.utils.logger import logger
from src.utils.mappers import mapper_entity
import src.controllers as controller
import src.schemas as schemas

router = APIRouter()

@cbv(router)
class EntityRouter:
    # dependency injection
    db: Session = Depends(get_db)

    user_dependency = Annotated[dict, Depends(get_current_user)]

    @router.post("/create")
    def create_entity(self, user: user_dependency, entity:schemas.EntityCreate ) -> Dict[str, Any]:
        """
        create a entity
        :return:
        """
        if user is None:
            raise HTTPException(status_code=401, detail='Autenticated neded')
        try:
            logger.info("entity creation process started")
            controller.entity.create(self.db, entity=entity)
            return {
                "type": "sucess",
                "message": "entity create successfull",
                "data": []
            }
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=400, detail=str(e))


    @router.get("/")
    def get_entities(self, user: user_dependency, location_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get all entities
        :return:
        """
        if user is None:
            raise HTTPException(status_code=401, detail='Autenticated neded')
        logger.info("get entities process started")
        response = {}

        if location_id:
            entities = controller.entity.get_by_location(self.db, location_id)
        else:
            entities = controller.entity.fetch_all_with_location(self.db)
        
        if entities:
            response = {
                    "type": "success",
                    "message": "successfully completed process",
                    "data": list(map(mapper_entity, entities)),
                    "total": len(entities)
            }
        else:
            response = {
                    "type": "error",
                    "message": "data not found",
                    "data": []
            }

        logger.info(response.get("message"))

        return response

    @router.get("/{id}")
    def get_entity(self, user: user_dependency, id:int) -> Dict[str, Any]:
        """
        Get a single entity
        :return:
        """
        if user is None:
            raise HTTPException(status_code=401, detail='Autenticated neded')
        logger.info("get entity process started")
        entity =  controller.entity.get_with_location(self.db, id)
        
        if not entity:
            logger.info("Entity not found")
            raise HTTPException(status_code=404, detail="Entity not found")
        
        logger.info("successfully completed process")
            
        return {
                "type": "sucess",
                "message": "successfully completed process",
                "data": mapper_entity(entity)
            }
    
    @router.put("/{id}")
    def update_entity(self, user: user_dependency, id: int, info: schemas.EntityUpdate) -> Dict[str, Any]:
        """
        Update a entity
        :return:
        """
        if user is None:
            raise HTTPException(status_code=401, detail='Autenticated neded')
        logger.info("update entity process started")

        try:
            entity = controller.entity.get(self.db, id)
            if not entity:
                logger.info("Entity not found")
                raise HTTPException(status_code=404, detail="Entity not found")
            update_entity = controller.entity.update(self.db, model_id=id, entity=info)
            logger.info("successfully completed process")
            return {
                "type": "success",
                "message": "successfully completed process",
                "data": mapper_entity(update_entity)
            }
        except HTTPException as http_error:
            raise http_error
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise HTTPException(status_code=500, detail="An error occurred while updating the entity")
    
    @router.put("/delete/{id}")
    def soft_delete_entity(self,user: user_dependency, id: int, info: schemas.EntitySoftDelete):
        """
        Soft delete an entity by setting the 'deleted' flag to True.
        """
        if user is None:
            raise HTTPException(status_code=401, detail='Autenticated neded')
        logger.info("delete entity process started")

        try:
            entity = controller.entity.get(self.db, id)
            if not entity:
                logger.info("Entity not found")
                raise HTTPException(status_code=404, detail="Entity not found")

            controller.entity.soft_delete(self.db, model_id=id, entity=info)

            logger.info("Entity deleted successfully")

            return {
                "type": "sucess",
                "message": "Entity deleted successfully",
                "data": []
            }
        
        except HTTPException as http_error:
            raise http_error
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise HTTPException(status_code=500, detail="An error occurred while deleting the entity")
        
    

    