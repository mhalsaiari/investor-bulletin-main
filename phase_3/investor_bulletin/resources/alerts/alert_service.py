""" Rule Service"""

"""_summary_
this file to write any business logic for the Rules
"""
from resources.alerts.alert_schema import AlertCreate
from resources.alerts.alert_dal import create_alert, get_alerts
from sqlalchemy.orm import session


def create_new_alert(alert: AlertCreate, db: session):
    return create_alert(alert=alert, db=db)


def get_all_alerts(db: session):
    return get_alerts(db)
