from typing import Any
from sqlalchemy.orm import Session, joinedload
from src.controllers.base import BaseController
import src.models as models
import src.schemas as schemas
from src.utils import Singleton

"""
This class is a CRUD class for the Data table.
"""

class EntityCRUD(
    
    BaseController[schemas.Entity, schemas.EntityCreate, schemas.EntityUpdate],
    metaclass=Singleton,
):
    def __init__(self):
        super().__init__(models.Entity)   

    def fetch_all_with_location(self, db: Session) -> list[tuple[Any]]:
        """
        Get records by its ID with related country information.
        :param db: Database session
        :return: Entity object with related country information
        """
        return  db.query(self.model_cls).filter(self.model_cls.deleted == False).options(joinedload(self.model_cls.country)).all()
    
    def get_with_location(self, db: Session, entity_id: int):
        """
        Get a record by its ID with related country information.
        :param db: Database session
        :param entity_id: ID of the entity to retrieve
        :return: Entity object with related country information
        """
        return db.query(self.model_cls).filter(self.model_cls.id == entity_id, self.model_cls.deleted == False).options(joinedload(self.model_cls.country)).first()
    
    def get_by_location(self, db: Session, location_id: int) -> list[tuple[Any]]:
        """
        Get a record by its ID with related country information.
        :param db: Database session
        :param location_id: ID of the location to retrieve
        :return: Entity object with related country information
        """
        return db.query(self.model_cls).filter(self.model_cls.locationId == location_id, self.model_cls.deleted == False).options(joinedload(self.model_cls.country)).all()
    
    def search_entity(self, db:Session, location_id: int, name: str):
        """
        Get a record by location and name with related country information.
        :param db: Database session
        :param location_id: ID of the location to retrieve
        :param name: Name of the Entity
        :return: Entity object with related country information
        """
        return db.query(self.model_cls).filter_by(entityName=name, locationId=location_id, deleted=False).first()

    
# Create a singleton instance of the DataCRUD class
entity = EntityCRUD()