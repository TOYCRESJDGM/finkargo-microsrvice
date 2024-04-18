import pytz
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean,  DateTime, JSON, ARRAY

from src.adapters.orm_base import OrmBaseModel
from sqlalchemy import event
from sqlalchemy import DDL


class Country(OrmBaseModel):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    alpha2Code = Column(String)
    alpha3Code = Column(String)
    capital = Column(String)
    region = Column(String)
    subregion = Column(String)
    population = Column(Integer)
    timezones = Column(ARRAY(String))
    area = Column(Integer)
    demonym = Column(String)
    nativeName = Column(String)
    currencies = Column(ARRAY(JSON))
    languages = Column(ARRAY(JSON))
    flag = Column(String)
    creationDate = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))
    ModificationDate = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))
    deleted = Column(Boolean, default=False)

restart_seq = DDL("ALTER SEQUENCE %(table)s_id_seq RESTART WITH 100;")

event.listen(
    Country.__table__, "after_create", restart_seq.execute_if(dialect="mysql")
)






