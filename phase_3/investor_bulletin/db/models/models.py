import time
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv
from resources.alert_rules.alert_rule_model import AlertRule
from resources.alerts.alert_model import Alert
import os
from sqlalchemy.orm import sessionmaker
from db.models.model_base import Base

load_dotenv


db_uri = os.getenv("DATABASE_URL")


try:
    engine = create_engine(db_uri, echo=False)
except Exception as err:
    print(f"Failed to create database engine: {str(err)}")
    raise


max_retries = 10
for attempt in range(max_retries):
    try:
        # In production, would use a migration tool to create tables.
        Base.metadata.create_all(engine)
        print(f"✅ Database tables created successfully")
        break
    except Exception as err:
        if attempt < max_retries - 1:
            wait_time = 2**attempt
            print(
                f"Connection failed (attempt {attempt+1}/{max_retries}): Retrying in {wait_time} seconds..."
            )
            time.sleep(wait_time)
            continue


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
