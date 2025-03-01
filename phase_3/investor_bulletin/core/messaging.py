import json
import os
import time
from amqpstorm import Connection
from dotenv import load_dotenv
from amqpstorm.exception import AMQPConnectionError, AMQPChannelError


load_dotenv()


RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
EXCHANGE = os.getenv("RABBITMQ_EXCHANGE_MARKET_DATA")
ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_MARKET_DATA_KEY")

# publish events to market_data queue using market_data_exchange
# queues, exchanges and bindings defined in definitions file


def publish_stock_data(message):

    retries = 0
    max_retries = 2
    channel = None
    while retries <= max_retries:
        try:
            conn = Connection(
                RABBITMQ_HOST,
                RABBITMQ_USER,
                RABBITMQ_PASSWORD,
                timeout=30,
                heartbeat=600,
            )
            channel = conn.channel(rpc_timeout=30)
            channel.confirm_deliveries()

            channel.basic.publish(
                exchange=EXCHANGE,
                routing_key=ROUTING_KEY,
                body=json.dumps(message),
                properties={"delivery_mode": 2},
            )
            print("Message published successfully.")
            return  # Exit on success
        except (AMQPConnectionError, AMQPChannelError) as err:

            print(f"Error during connection or publish {retries + 1} failed: {err}")
            retries += 1
            time.sleep(2**retries)
            conn.close()


# I have a lot of issues with connection, I was getting the below error

# Error publishing message: rpc requests abb32620-4bb0-4b92-92a0-4c72c174741d (Channel.OpenOk) took too long,

# thus i have added retry mechanism and increased timeout for connection and channel
