""" Alert Rule  DAL"""
"""_summary_
this file is to right any ORM logic for the Alert Rule model
"""
import datetime
from resources.alert_rules.alert_rule_schema import AlertRuleCreate, AlertRuleUpdate
from db.models import AlertRule

def create_alert_rule( rule: AlertRuleCreate, db):
    new_rule = AlertRule(name=rule.name, threshold_price=rule.threshold_price,symbol=rule.symbol)

    db.add(new_rule)
    db.commit()
    return new_rule

def update_alert_rule( id: int, rule: AlertRuleUpdate, db):


    existing_rule = db.query(AlertRule).filter(AlertRule.id == id, AlertRule.deleted_at.is_(None)).first()
    # if rule does not exists raise error
    if not existing_rule:
        raise ValueError("Alert rule not found or already deleted")

    # Update only the provided fields .
    update_data = rule.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_rule, key, value)

    db.commit()
    db.refresh(existing_rule)  # Refresh to get updated fields from the database.
    return existing_rule

def delete_alert_rule( id: int, db):

    rule = db.query(AlertRule).filter(AlertRule.id == id, AlertRule.deleted_at.is_(None)).first()
    if not rule:
        raise ValueError("Alert rule not found or already deleted")

    rule.deleted_at = datetime.datetime.now(datetime.UTC)
    db.commit()
    db.refresh(rule)
    return rule

def get_all_alert_rules(db):
    return db.query(AlertRule).filter(AlertRule.deleted_at.is_(None)).all()
