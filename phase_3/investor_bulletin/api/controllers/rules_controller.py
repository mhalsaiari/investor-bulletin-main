from fastapi import APIRouter, Depends, HTTPException
from fastapi import APIRouter
from typing import List
from resources.alert_rules.alert_rule_service import (
    create_new_rule,
    update_rule,
    delete_rule,
    get_all_rules,
)
from resources.alert_rules.alert_rule_schema import (
    AlertRuleCreate,
    AlertRuleUpdate,
    AlertRuleSchema,
)
from sqlalchemy.orm import session
from db.models.models import get_db


router = APIRouter()


# POST /alert-rules
# Creates an alert rule specific to a user with the following properties: name, threshold price, and symbol.
@router.post("/")
def create_alert_rule(alert_rule: AlertRuleCreate, db: session = Depends(get_db)):
    try:
        create_new_rule(alert_rule, db=db)
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
    return {"message": "Alert rule created successfully"}


# PATCH /alert-rules/{id}
# Update an alert rule by ID.
@router.patch("/{id}")
def update_alert_rule(
    id: int, alert_rule: AlertRuleUpdate, db: session = Depends(get_db)
):
    update_data = alert_rule.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Must update at least one field")
    try:
        update_rule(id, alert_rule, db=db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
    return {"message": "Alert rule updated successfully"}


# DELETE /alert-rules/{id}
# Deletes an alert rule by ID.
# soft delete
@router.delete("/{id}")
def delete_alert_rule(id: int, db: session = Depends(get_db)):
    try:
        delete_rule(id, db=db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
    return {"message": "Alert rule deleted successfully"}


# GET /alert-rules
# Returns all alert rules
# Response model added here, so that id number does not rounded.
@router.get("/", response_model=List[AlertRuleSchema])
def get_alert_rules(db: session = Depends(get_db)):
    try:
        all_rules = get_all_rules(db=db)
        return all_rules
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
