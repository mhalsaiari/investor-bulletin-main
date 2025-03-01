""" Alert Schema """

"""_summary_
This file to abstract any validation logic for the Alerts
"""
from pydantic import BaseModel, field_validator
from typing import Optional
from resources.alert_rules.alert_rule_schema import AlertRuleSchema


class AlertCreate(BaseModel):
    alert_rule_id: int


class AlertSchema(BaseModel):
    id: str
    alert_rule_id: str
    alert_rule: Optional[AlertRuleSchema]

    class Config:
        orm_mode = True

    @field_validator("id", mode="before")
    def convert_id_to_str(cls, v):
        return str(v)

    @field_validator("alert_rule_id", mode="before")
    def convert_alert_rule_id_to_str(cls, v):
        return str(v)
