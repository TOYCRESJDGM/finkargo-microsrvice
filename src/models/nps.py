from datetime import datetime
import pytz

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean

from src.adapters.orm_base import OrmBaseModel
from sqlalchemy import event
from sqlalchemy.orm import relationship
from sqlalchemy import DDL

"""
ORM class to interact with the nps table in the database
"""

class NPS(OrmBaseModel):
    __tablename__ = 'nps'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    score = Column(Integer, nullable=False)
    positionId = Column(Integer, ForeignKey('position.id'), nullable=False)
    userId = Column(Integer, ForeignKey('user.id'), nullable=True)
    creationDate = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))
    ModificationDate = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))
    deleted = Column(Boolean, default=False)

    position = relationship("Position")
    user = relationship("User")


restart_seq = DDL("ALTER SEQUENCE %(table)s_id_seq RESTART WITH 100;")

event.listen(
    NPS.__table__, "after_create", restart_seq.execute_if(dialect="mysql")
)