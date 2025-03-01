from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import session
from db.models.models import get_db
from resources.alerts.alert_service import get_all_alerts


from resources.alerts.alert_schema import AlertSchema
router = APIRouter()

# GET /alerts
# Returns all alerts specific to a user
@router.get("/", response_model=List[AlertSchema])
def get_alerts(db: session= Depends(get_db)):
    try:
      all_alerts = get_all_alerts(db=db)
      return all_alerts
    except Exception as err:
       raise HTTPException(status_code=500, detail=str(err))


#1049529436051668993
#1049529436051669000
