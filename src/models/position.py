from datetime import datetime
import pytz

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean

from src.adapters.orm_base import OrmBaseModel
from sqlalchemy import event
from sqlalchemy.orm import relationship
from sqlalchemy import DDL

"""
ORM class to interact with the Position table in the database
"""

class Position(OrmBaseModel):
    __tablename__ = 'position'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    positionName = Column(String(100), nullable=False)
    entityId = Column(Integer, ForeignKey('entity.id'), nullable=False)
    creationDate = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))
    ModificationDate = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))
    deleted = Column(Boolean, default=False)

    entity = relationship("Entity")


restart_seq = DDL("ALTER SEQUENCE %(table)s_id_seq RESTART WITH 100;")

event.listen(
    Position.__table__, "after_create", restart_seq.execute_if(dialect="mysql")
)