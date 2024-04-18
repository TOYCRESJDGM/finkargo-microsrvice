from fastapi import Depends, HTTPException, Header
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session
from typing import Optional, Annotated, Dict, Any

from src.utils.encrypt import get_current_user, decode_token

from src.adapters.mysql_adapter import get_db
from src.utils.logger import logger
from src.utils.mappers import mapper_nps
import src.controllers as controller
import src.schemas as schemas

router = InferringRouter()

@cbv(router)
class NpsRouter:
    # dependency injection
    db: Session = Depends(get_db)

    user_dependency = Annotated[dict, Depends(get_current_user)]

    @router.post("/register")
    def register_nps(self, nps: schemas.NpsCreate, authorization: str = Header(None)) -> Dict[str, Any]:
        """
        register a nps
        :return:
        """
        try:
            if authorization:
                token = authorization.replace("Bearer ", "")
                payload = decode_token(token)
                if payload is not None:
                    user_id = payload['sub']
                    nps.userId = user_id
                
            logger.info("nps register process started")
            controller.nps.create(self.db, entity=nps)
            return {
                "type": "sucess",
                "message": "nps register successfull",
                "data": []
            }
               
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=400, detail=str(e))


    @router.get("/")
    def get_information_nps(self, user: user_dependency ,position_name: Optional[str] = None, entity_id: Optional[int] = None, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get all nps
        :return:
        """
        if user is None:
            raise HTTPException(status_code=401, detail='Autenticated neded')
        
        logger.info("get nps process started")

        records_nps = controller.nps.fetch_all_with_position_information(self.db, position_name, entity_id, user_id)
        
        if not records_nps:
            logger.info("Nps information not found")
            raise HTTPException(status_code=404, detail="position not found")
        
        logger.info("successfully completed process")
            
        return {
                "type": "success",
                "message": "successfully completed process",
                "data": list(map(mapper_nps, records_nps)),
                "total": len(records_nps)
        }
    

    @router.get("/general/reports")
    def general_reports(self, option: int = 1) -> Dict[str, Any]:
        """
        Get all nps
        :return:
        """
        if option:
            print("test")
        logger.info("get nps reports started")

        report_response = controller.nps.generate_reports(self.db, option)
        
        if not report_response:
            logger.info("Nps information not found")
            raise HTTPException(status_code=404, detail="position not found")
        
        logger.info("successfully completed process")
            
        return {
                "type": "success",
                "message": "successfully completed process",
                "data": report_response,
                "total": len(report_response)
        }
    

    @router.get("/reports/low_score/{entity_id}")
    def reports_low_score(self, entity_id: int) -> Dict[str, Any]:
        """
        Gets all the users who have rated the company low
        :return:
        """
        logger.info("get nps reports low score for entity")

        records_nps = controller.nps.get_low_score(self.db, entity_id)
        
        if not records_nps:
            logger.info("Nps information not found")
            raise HTTPException(status_code=404, detail="position not found")
        
        logger.info("successfully completed process")
            
        return {
                "type": "success",
                "message": "successfully completed process",
                "data": list(map(mapper_nps, records_nps)),
                "total": len(records_nps)
        }