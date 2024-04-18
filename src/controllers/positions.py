from typing import Any
from sqlalchemy.orm import Session, joinedload, Query
from src.controllers.base import BaseController
import src.models as models
import src.schemas as schemas
from src.utils import Singleton

"""
This class is a CRUD class for the Position table.
"""

class PositionCRUD(
    
    BaseController[schemas.Position, schemas.PositionCreate, schemas.PositionUpdate],
    metaclass=Singleton,
):
    def __init__(self):
        super().__init__(models.Position)   

    def fetch_all_with_entity(self, db: Session) -> list[tuple[Any]]:
        """
        Get a records by its ID with related entity information.
        :param db: Database session
        :return: position object with related entity information
        """
        return  db.query(self.model_cls).filter(self.model_cls.deleted == False).options(joinedload(self.model_cls.entity)).all()
    
    def search_position(self, db: Session, entity_id: int, name: str) -> list[tuple[Any]]:
        """
        Get a record by its ID with related entity information.
        :param db: Database session
        :param entity_id: ID of the entity to retrieve
        :param name: Name of the position to retrieve
        :return: position object with related entity information
        """
        query: Query = db.query(self.model_cls).filter(self.model_cls.deleted == False).options(joinedload(self.model_cls.entity))

        if entity_id:
            query = query.filter(self.model_cls.entityId == entity_id)
        if name:
            query = query.filter(self.model_cls.positionName == name)

        return query.all()
        
        
    def get_with_entity(self, db: Session, position_id: int):
        """
        Get a record by its ID with related entity information.
        :param db: Database session
        :param position_id: ID of the position to retrieve
        :return: Position object with related entity information
        """
        return db.query(self.model_cls).filter(self.model_cls.id == position_id, self.model_cls.deleted == False).options(joinedload(self.model_cls.entity)).first()
          
    
# Create a singleton instance of the PositionCRUD class
position = PositionCRUD()