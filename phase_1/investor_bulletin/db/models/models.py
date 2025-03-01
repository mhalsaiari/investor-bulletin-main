from sqlalchemy import create_engine
from dotenv import load_dotenv
from resources.alert_rules.alert_rule_model import AlertRule
from resources.alerts.alert_model import Alert
import os
from sqlalchemy.orm import sessionmaker
from db.models.model_base import Base

load_dotenv

db_uri = os.getenv("DATABASE_URL")


engine = create_engine(db_uri, echo=True)

# In production, would use a migration tool to create tables.
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
