import json
import os
from socket import timeout
from amqpstorm import Connection
from dotenv import load_dotenv


load_dotenv()

# publish events to market_data queue using market_data_exchange
# queues, exchanges and bindings defined in definitions file

def publish_stock_data(message):
    broker = Connection(os.getenv('RABBITMQ_HOST'), os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASSWORD'), timeout=30)
    channel = broker.channel()


    channel.basic.publish(
        exchange=os.getenv('RABBITMQ_EXCHANGE_MARKET_DATA'),
        routing_key=os.getenv('RABBITMQ_ROUTING_MARKET_DATA_KEY'),
        body=json.dumps(message)
    )

    broker.close()
