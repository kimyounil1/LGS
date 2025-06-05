from fastapi import APIRouter
from LGS.schemas.forecast import ForecastResponse
from LGS.services.forecast_service import forecast_stock_logic

router = APIRouter()

@router.get("/stocks/forecast", response_model=ForecastResponse)
async def forecast_stock(ticker: str = "TSLA"):
    return forecast_stock_logic(ticker)