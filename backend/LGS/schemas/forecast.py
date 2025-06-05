from pydantic import BaseModel
from typing import List

class PricePoint(BaseModel):
    date: str
    price: float

class ForecastResponse(BaseModel):
    ticker: str
    today: float
    historical: List[PricePoint]
    forecast: List[PricePoint]
    signal: str
    summary: str
