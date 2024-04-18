from typing import Any
from sqlalchemy.orm import Session, join, joinedload, Query
from src.controllers.base import BaseController
import src.models as models
import src.schemas as schemas
from src.utils import Singleton
from collections import Counter, defaultdict

"""
This class is a CRUD class for the nps table.
"""

class NpsCRUD(
    
    BaseController[schemas.Nps, schemas.NpsCreate, schemas.NpsUpdate],
    metaclass=Singleton,
):
    def __init__(self):
        super().__init__(models.NPS)   

    def fetch_all_with_position_information(self, db: Session, position_name: str= None, entity_id: int = None, user_id: int = None) -> list[tuple[Any]]:
        """
        Get a records by its ID with related position information.
        :param db: Database session
        :return: Nps object with related position information
        """
        query: Query = db.query(self.model_cls).filter(self.model_cls.deleted == False)

        # Join with the position relationship
        query = query.join(self.model_cls.position)

        # Filter by position name, if provided
        if position_name:
            query = query.filter(models.Position.positionName == position_name)

        # Filter by entity ID, if provided
        if entity_id:
            query = query.filter(models.Position.entityId == entity_id)

        # Filter by user ID, if provided
        if user_id:
            query = query.filter(self.model_cls.userId == user_id)

        return query.all()
        
    def get_low_score(self, db: Session, entity_id: int):
        """
        Get a records related to the low score by entity ID with user information.
        :param db: Database session
        :param entity_id: ID of the entity to retrieve
        :return: Nps object with related position information
        """
        query = (
            db.query(self.model_cls)
            .filter(self.model_cls.deleted == False, self.model_cls.score < 4)
            .join(self.model_cls.position)
            .options(joinedload(self.model_cls.user))
        )

        if entity_id:
            query = query.filter(models.Position.entityId == entity_id)

        return query.all()
    
    
    def get_report_records(self, db: Session):
        """
        Get a records for reports with user and position information.
        :param db: Database session
        :return: Nps object swith related position and user information
        """
        query: Query = db.query(self.model_cls).filter(self.model_cls.deleted == False).options(joinedload(self.model_cls.user), joinedload(self.model_cls.position))

        return query.all()
    

    def process_top_3_scores(self, db: Session, score_type: str):
        """
        Get a dictionary with information on the 3 main countries for promoters or detractors..
        :param db: Database session
        :param score_type: Type of the score
        :return: Dict related nps information
        """
        response = []
        records = self.get_report_records(db)

        surveys_per_country = Counter()
        scores_per_country = Counter()

        for record in records:
            country = record.position.entity.country.name
            surveys_per_country[country] += 1
            if (score_type == "detractors" and record.score <= 6) or (score_type == "promoters" and record.score > 8):
                scores_per_country[country] += 1
            
    
        top_countries = surveys_per_country.most_common(3)

        for country, surveys_count in top_countries:
            score_count = scores_per_country[country]
            response.append({
                "country": country, 
                "surveys": surveys_count, 
                score_type: score_count
            })
    
        return response
    
    def promoters_position(self, db: Session):
        """
        Get a dictionary with the position promoters. ..
        :param db: Database session
        :return: Dict related nps information
        """
        response = []
        records = self.get_report_records(db)

        surveys_per_position = Counter()
        promoters_per_position = Counter()

        for record in records:
            position_id = record.position.id
            position_name = record.position.positionName
            surveys_per_position[(position_id, position_name)] += 1
            if record.score > 8:
                promoters_per_position[(position_id, position_name)] += 1

        for (position_id, position_name), surveys_count in surveys_per_position.items():
            promoters_count = promoters_per_position[(position_id, position_name)]
            response.append({
                "positionId": position_id, 
                "positionName": position_name,
                "surveys": surveys_count, 
                "promoters": promoters_count
            })

        return response
    
    def classify_surveys_by_month(self, db: Session):
        response = defaultdict(list)
        records = self.get_report_records(db)

        for record in records:
            # Obtener el mes y el país de la encuesta
            month = record.creationDate.strftime("%Y-%m")
            country = record.position.entity.country.name

            # Determinar si es detractor, promotor o neutral
            score_type = "neutral"
            if record.score <= 6:
                score_type = "detractor"
            elif record.score > 8:
                score_type = "promoter"

            # Actualizar la información para el mes y país correspondiente
            response[(month, country)].append(score_type)

        # Encontrar el detractor y promotor más alto para cada país en cada mes
        for key, scores in response.items():
            detractors_count = scores.count("detractor")
            promoters_count = scores.count("promoter")
            neutral_count = scores.count("neutral")
            total_surveys = len(scores)

            highest_score = max(detractors_count, promoters_count)
            if highest_score == detractors_count:
                highest_type = "detractor"
                highest_count = detractors_count
            elif highest_score == promoters_count:
                highest_type = "promoter"
                highest_count = promoters_count
            else:
                highest_type = "neutral"
                highest_count = neutral_count

            # Actualizar la respuesta con el detractor o promotor más alto
            response[key] = {
                "month": key[0],
                "country": key[1],
                "totalSurveys": total_surveys,
                "highestType": highest_type,
                "highestCount": highest_count,
                "detractorsCount": detractors_count,
                "promotersCount": promoters_count,
                "neutralCount": neutral_count
            }

        return list(response.values())
    
    def generate_reports(self, db: Session, option: int):

        if option == 1:
            response = self.classify_surveys_by_month(db)
        elif option == 2:
            response = self.process_top_3_scores(db, "promoters")
        elif option == 3:
            response = self.process_top_3_scores(db, "detractors")
        elif option == 4:
            response = self.promoters_position(db)

        
        return response


                

    


        
    
    
    
# Create a singleton instance of the NpsCRUD class
nps = NpsCRUD()