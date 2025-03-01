""" Alert DAL"""
"""_summary_
this file is to right any ORM logic for the Alert model
"""
from resources.alerts.alert_schema import AlertCreate
from db.models import Alert
from sqlalchemy.orm import joinedload

def create_alert( alert: AlertCreate, db):
    new_alert = Alert(alert_rule_id=alert.alert_rule_id)
    db.add(new_alert)
    db.commit()
    return new_alert

def get_alerts(db):
    return db.query(Alert).options(joinedload(Alert.alert_rule)).all()
