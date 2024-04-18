from datetime import datetime
import pytz

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean

from src.adapters.orm_base import OrmBaseModel
from sqlalchemy import event
from sqlalchemy import DDL

"""
ORM class to interact with the user table in the database
"""

class User(OrmBaseModel):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userName = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    creationDate = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))
    ModificationDate = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))
    deleted = Column(Boolean, default=False)


restart_seq = DDL("ALTER SEQUENCE %(table)s_id_seq RESTART WITH 100;")

event.listen(
    User.__table__, "after_create", restart_seq.execute_if(dialect="mysql")
)