""" Alert Model """

from db.models.model_base import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_rule_id = Column(Integer, ForeignKey("alert_rules.id"))
    alert_rule = relationship("AlertRule", back_populates="alerts")
