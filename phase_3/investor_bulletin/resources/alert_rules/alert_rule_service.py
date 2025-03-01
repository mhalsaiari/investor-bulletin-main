""" Alert Rule Service"""

"""_summary_
this file to write any business logic for the Alert Rules
"""

from resources.alert_rules.alert_rule_schema import AlertRuleCreate, AlertRuleUpdate
from resources.alert_rules.alert_rule_dal import (
    create_alert_rule,
    update_alert_rule,
    delete_alert_rule,
    get_all_alert_rules,
)
from sqlalchemy.orm import session


def create_new_rule(rule: AlertRuleCreate, db: session):
    return create_alert_rule(rule=rule, db=db)


def update_rule(id: int, rule: AlertRuleUpdate, db: session):
    return update_alert_rule(id=id, rule=rule, db=db)


def delete_rule(id: int, db: session):
    return delete_alert_rule(id=id, db=db)


def get_all_rules(db: session):
    return get_all_alert_rules(db)
