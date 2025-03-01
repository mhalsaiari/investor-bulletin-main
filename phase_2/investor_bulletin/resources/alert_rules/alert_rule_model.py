from db.models.model_base import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship

class AlertRule(Base):
    __tablename__ = "alert_rules"

    # Production application should use UUID instead, but for the simplicity used integers and to have advantage of auto-Increment functionality
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    threshold_price = Column(Float, nullable=False)
    symbol = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationship: One AlertRule can have many Alerts.
    alerts = relationship("Alert", back_populates="alert_rule")
