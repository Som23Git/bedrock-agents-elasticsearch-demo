# routers/search.py
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from elasticsearch import exceptions as es_exceptions
from datetime import datetime
import os

from schemas.models import TripSummary, TripResponse
from utils.es_client import es

router = APIRouter(prefix="", tags=["Search Trips"])

INDEX_NAME = os.getenv("INDEX_NAME", "notebook_index_semantic_v1")

@router.get("/searchTrips", response_model=TripResponse)
def search_trips(
    model_text: str = Query(..., description="Text query from the user, e.g. 'last 5 trips in 2025'"),
    size: int = Query(5, description="Number of trips to return"),
    date_gte: str = Query(None, description="Start date in YYYY-MM-DD format"),
    date_lte: str = Query(None, description="End date in YYYY-MM-DD format"),
    sort_order: str = Query("desc", description="Sort order by trip_date, either 'asc' or 'desc'")
):
    try:
        filters = []
        if date_gte or date_lte:
            range_filter = {}
            if date_gte:
                range_filter["gte"] = date_gte
            if date_lte:
                range_filter["lte"] = date_lte
            filters.append({"range": {"trip_date": range_filter}})

        response = es.search(
            index=INDEX_NAME,
            knn={
                "field": "trip_summary.inference.chunks.embeddings",
                "query_vector_builder": {
                    "text_embedding": {
                        "model_id": "bedrock-embeddings",
                        "model_text": model_text
                    }
                },
                "k": size,
                "num_candidates": 50
            },
            query={
                "bool": {
                    "filter": filters
                }
            },
            sort=[
                {"trip_date": {"order": sort_order}}
            ],
            size=size,
            source={
                "includes": [
                    "trip_summary.text",
                    "driver",
                    "total_fare_inr",
                    "trip_date"
                ]
            },
        )

        hits = response.get("hits", {}).get("hits", [])
        if not hits:
            return TripResponse(summary_text="No trips found for your query.", trips=[])

        trips = []
        summary_lines = []

        for h in hits:
            src = h["_source"]
            trip_date = src.get("trip_date")
            driver = src.get("driver")
            fare = src.get("total_fare_inr")
            trips.append(TripSummary(trip_date=trip_date, driver=driver, fare=round(fare, 2)))

            date_str = datetime.strptime(trip_date, "%Y-%m-%d").strftime("%d %b %Y")
            summary_lines.append(f"• On {date_str}, driven by {driver}, total fare ₹{fare:.2f}")

        summary_text = f"I found {len(trips)} trip(s):\n" + "\n".join(summary_lines)

        return TripResponse(summary_text=summary_text, trips=trips)

    except es_exceptions.ConnectionTimeout:
        return JSONResponse(
            status_code=504,
            content={"summary_text": "Request to Elasticsearch timed out. Please try again later.", "trips": []}
        )
    except es_exceptions.ApiError as e:
        return JSONResponse(
            status_code=500,
            content={"summary_text": f"Elasticsearch error: {str(e)}", "trips": []}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"summary_text": f"Unexpected error occurred: {str(e)}", "trips": []}
        )