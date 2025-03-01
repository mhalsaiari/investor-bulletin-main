from fastapi import APIRouter, HTTPException, Query
from fastapi import APIRouter
from resources.market.market_service import MarketService
from resources.market.market_schema import MarketItem
from typing import List

router = APIRouter()
service = MarketService()


@router.get("/", response_model=List[MarketItem])
def get_market_data_route(
    symbols: List[str] = Query(
        ["AAPL", "MSFT", "GOOG", "AMZN", "META"], description="List of symbols"
    )
):
    try:
        items = service.get_market_data(symbols)
        return items
    except Exception as err:
        # If an error occurs in the service, return an HTTP error with the message.
        raise HTTPException(status_code=500, detail=str(err))
