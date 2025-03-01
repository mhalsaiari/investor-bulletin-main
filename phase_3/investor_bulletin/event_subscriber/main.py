import json
import time
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from pika import BlockingConnection, PlainCredentials, ConnectionParameters
import os
from resources.alert_rules.alert_rule_service import get_all_rules
from db.models.models import get_db
from resources.alerts.alert_service import create_new_alert
from resources.alerts.alert_schema import AlertCreate
from pika.exceptions import AMQPConnectionError

# Create a connection object to start consuming events


load_dotenv()

user = os.getenv("RABBITMQ_USER")
password = os.getenv("RABBITMQ_PASSWORD")
host = os.getenv("RABBITMQ_HOST")
port = os.getenv("RABBITMQ_PORT")

credentials = PlainCredentials(user, password)
parameters = ConnectionParameters(host, port, "/", credentials)


def init_subscriber():
    max_retries = 3
    retry_delay = 5
    for attempt in range(max_retries):
        try:
            connection = BlockingConnection(parameters)
            channel = connection.channel()
            return channel, connection
        except AMQPConnectionError:
            if attempt < max_retries - 1:
                print(
                    f"Connection failed, retrying in {retry_delay} sec... ({attempt+1}/{max_retries})"
                )
                time.sleep(retry_delay)
                continue
            raise
    raise RuntimeError("Failed to connect to RabbitMQ after multiple attempts")


def on_event(ch, method, properties, body):

    message = json.loads(body)
    if message.get("eventName") == "STOCK_DATA":
        print("Processing STOCK_DATA event:", message)
        try:
            db = next(get_db())
            user_rules = get_all_rules(db=db)

            # Convert rules to dictionary form
            rules = [jsonable_encoder(rule) for rule in user_rules]

            # Build a lookup dict, key is symbol, value is rule data
            rule_lookup = {rule["symbol"]: rule for rule in rules}

            for stock in message["eventData"]["stock_data"]:

                symbol = stock["symbol"]
                price = stock["price"]

                # Look up the rule for this symbol
                if symbol in rule_lookup:

                    rule_data = rule_lookup[symbol]
                    threshold = rule_data["threshold_price"]

                    if price > threshold:

                        print(
                            f"{symbol} price {price} is higher than threshold {threshold}"
                        )
                        alert_payload = AlertCreate(
                            alert_rule_id=rule_lookup[symbol]["id"]
                        )
                        create_new_alert(alert_payload, db)

                    elif price < threshold:

                        print(
                            f"{symbol} price {price} is lower than threshold {threshold}"
                        )
                        alert_payload = AlertCreate(
                            alert_rule_id=rule_lookup[symbol]["id"]
                        )
                        create_new_alert(alert_payload, db)

        except Exception as e:
            print(f"Error occurred while fetching data: {e}")
        finally:
            db.close()
    else:
        print("Ignoring message with event:", message.get("eventName"))
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":

    try:
        channel, connection = init_subscriber()
        channel.basic_consume(queue="market_data", on_message_callback=on_event)
        print("Starting consumer...")
        channel.start_consuming()
    except AMQPConnectionError as e:
        print(f"RabbitMQ connection error: {str(e)}")
    except KeyboardInterrupt:
        print("Interrupted by user, stopping...\n")
        channel.stop_consuming()
    finally:
        connection.close()
