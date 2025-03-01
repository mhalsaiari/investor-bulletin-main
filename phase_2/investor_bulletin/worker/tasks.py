from fastapi.encoders import jsonable_encoder
from worker.app import app
from resources.market.market_service import MarketService
from core.messaging import publish_stock_data
from datetime import datetime, timezone
market_service = MarketService()

@app.task()
def get_market_data():
    market_data = None
    try:
        symbols = ["AAPL", "MSFT", "GOOG", "AMZN", "META"]
        market_data = market_service.get_market_data(symbols)
    except Exception as err:
        print(f"Error fetching market data: {err}")
    publish_stock_data_event(market_data)

    return market_data

def publish_stock_data_event(market_data):
    # Publish event
    serializable_data = jsonable_encoder(market_data)
    message_body = {
        "eventName": "STOCK_DATA",
        "eventData": {
            "stock_data": serializable_data
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    publish_stock_data(message_body)
