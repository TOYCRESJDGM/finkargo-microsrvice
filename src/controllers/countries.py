import requests

import src.models as models
from src.utils.settings import ( URL_COUNTRIES ) 

from sqlalchemy.orm import Session
from src.controllers.base import BaseController
import src.models as models
import src.schemas as schemas
from src.utils import Singleton

"""
This class is a CRUD class for the country table.
"""

class CountryCRUD(
    
    BaseController[schemas.Country, schemas.CountryCreate, None],
    metaclass=Singleton,
):
    def __init__(self):
        super().__init__(models.Country)
        self.loaded = False
        self.countries = []

    def load_countries(self, db: Session):
        """
        load countries.
        :param db:
        :return:
        """
        url = URL_COUNTRIES
        response = requests.get(url)
        if response.status_code == 200:
            countries_data = response.json()
            for country_data in countries_data:
                country = models.Country(
                    name=country_data["name"],
                    alpha2Code=country_data["alpha2Code"],
                    alpha3Code=country_data["alpha3Code"],
                    capital=country_data.get("capital", ""),
                    region=country_data.get("region", ""),
                    subregion=country_data.get("subregion", ""),
                    population=country_data.get("population", 0),
                    area=country_data.get("area", 0.0),
                    timezones=country_data.get("timezones", []),
                    demonym=country_data.get("demonym", ""),
                    nativeName=country_data.get("nativeName", ""),
                    currencies=country_data.get("currencies", []),
                    languages=country_data.get("languages", []),
                    flag=country_data["flag"],
                )
                self.countries.append(country)   
            self.loaded = True

            CountryCRUD.create_batch(self,db=db,entities=self.countries)
        
# Create a singleton instance of the Country class
country = CountryCRUD()
        
        
        