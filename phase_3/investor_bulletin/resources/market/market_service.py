# resources/market/market_service.py
import requests
from requests.exceptions import HTTPError
import time
import os
from dotenv import load_dotenv
from typing import List
from resources.market.market_schema import MarketItem

load_dotenv()


class MarketService:
    def __init__(self):
        self.api_url = "https://twelve-data1.p.rapidapi.com/price"
        self.headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": os.getenv("RAPIDAPI_HOST"),
        }
        self.session = requests.Session()
        self.max_retries = 3
        self.retry_delay = 60  # Base delay in seconds

    def get_market_data(self, symbols: List[str]) -> List[MarketItem]:
        items = []
        for symbol in symbols:
            price_str = self.get_price_for_symbol(symbol)
            try:
                price = float(price_str)
            except (TypeError, ValueError):
                price = 0.0
            items.append(MarketItem(symbol=symbol, price=price))
        return items

    def get_price_for_symbol(self, symbol: str) -> str:
        querystring = {"symbol": symbol, "outputsize": "30", "format": "json"}
        for attempt in range(self.max_retries + 1):
            try:
                print(f"Fetching data for {symbol}")
                response = self.session.get(
                    self.api_url, headers=self.headers, params=querystring
                )
                response.raise_for_status()
                # Expecting the API to return - {"price": "245.55"}
                return response.json()["price"]
            except HTTPError as http_err:
                status_code = http_err.response.status_code
                if status_code == 429:
                    print(
                        f"Rate limited on {symbol}, retrying in {self.retry_delay}s..."
                    )
                    time.sleep(self.retry_delay)
                    return self.get_price_for_symbol(symbol)  # retry the request
                else:
                    raise Exception(f"HTTP error occurred for {symbol}: {http_err}")
            except Exception as err:
                raise Exception(f"General error occurred for {symbol}: {err}")

    def close(self):
        self.session.close()

    def __exit__(self, *args):
        self.close()


# why this approach
# - segregation of concerns
# - better error handling
# - retry mechanism for single symbol
# - better in unit tests

"""
At the beginning I tried to combine it as one function, but later on i have discovered that API token consumption is per parameter instead of API call, therefore i have implment it as two sprate functions and this approach is better for having retry machnism since its going to use only one symbol.
Combine it in one function also make reuseability and modification more complex, this approach it more simple and readble, also "get_price_for_symbol" function can be used in multiple component as needed
"""
