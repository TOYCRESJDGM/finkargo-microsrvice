from typing import List, Dict
from datetime import datetime
from pydantic import BaseModel

class CountrySchema(BaseModel):
    name: str
    alpha2Code: str
    alpha3Code: str
    capital: str
    region: str
    subregion: str
    population: int
    area: float
    timezones: List[str]
    demonym: str
    nativeName: str
    currencies: List[Dict]
    languages: List[Dict]
    flag: str
    creationDate: datetime = datetime.now()
    ModificationDate: datetime = datetime.now()

class CountryCreate(CountrySchema):
    pass

class Country(CountrySchema):
    country_id: int = None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True