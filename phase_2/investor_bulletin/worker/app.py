import os
from celery import Celery
from dotenv import load_dotenv

# Create a celery app object to start your workers
load_dotenv()

user = os.getenv('RABBITMQ_USER')
password = os.getenv('RABBITMQ_PASSWORD')
host = os.getenv('RABBITMQ_HOST')
port = os.getenv('RABBITMQ_PORT')

url = f"pyamqp://{user}:{password}@{host}:{port}/"

def create_celery_app():
  app = Celery(
    'investor',
    broker= url
  )
  app.conf.include = ['worker.tasks']
  app.conf.timezone = 'UTC'
  app.conf.beat_schedule = {
        'fetch-market-data-every-5-minutes': {
            'task': 'worker.tasks.get_market_data',
            'schedule': 300.0,  # Every 300 seconds (5 minutes)
        },
  }
  return app


app = create_celery_app()
