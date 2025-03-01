""" Alert Rule Schema """
"""_summary_
This file to abstract any validation logic for the Alert Rules
"""
from datetime import UTC, datetime
from typing import Optional
from pydantic import BaseModel, field_validator

# creat alert shema
class AlertRuleCreate(BaseModel):
    name: str
    threshold_price: float
    symbol: str

# update alert shema
class AlertRuleUpdate(BaseModel):
    name: Optional[str] = None
    threshold_price: Optional[float] = None
    symbol: Optional[str] = None

# since we used integer for the id, when getting all alerts rules json encoding rounded the id number
class AlertRuleSchema(BaseModel):
    id: str
    name: str
    threshold_price: float
    symbol: str
    created_at: datetime
    updated_at: datetime

    @field_validator("id", mode="before")
    def convert_id_to_str(cls, v):
        return str(v)
