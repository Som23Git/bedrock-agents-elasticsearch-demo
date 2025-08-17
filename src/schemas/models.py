# schemas/models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class TripSummary(BaseModel):
    trip_date: str = Field(..., example="2025-07-12")
    driver: str = Field(..., example="Abdul")
    fare: float = Field(..., example=365.45)

class TripResponse(BaseModel):
    summary_text: str
    trips: List[TripSummary] = []

class SearchTripQuery(BaseModel):
    model_text: str = Field(..., description="Text to semantically search trips")
    size: Optional[int] = Field(5, description="Number of trips to return")
    date_gte: Optional[str] = Field(None, description="Start date in YYYY-MM-DD")
    date_lte: Optional[str] = Field(None, description="End date in YYYY-MM-DD")
    sort_order: Optional[str] = Field("desc", description="Sort order: asc or desc")
