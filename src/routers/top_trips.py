# Updated `top_trips.py` with new `/stats` endpoints for total fare, duration, and distance.

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from elasticsearch import exceptions as es_exceptions
from utils.es_client import es
from schemas.models import TripSummary, TripResponse
from datetime import datetime
import os

router = APIRouter(prefix="/topTrips", tags=["Top Trips"])
INDEX_NAME = os.getenv("INDEX_NAME", "notebook_index_semantic_v1")


@router.get("/byField", response_model=TripResponse)
def get_top_trips(
    field: str = Query(..., description="Field to sort by (e.g. total_fare_inr, duration_minutes, distance_km, promotion_inr)"),
    sort_order: str = Query("desc", description="Sort order: asc or desc"),
    date_gte: str = Query("2025-01-01", description="Start date"),
    date_lte: str = Query("2025-12-31", description="End date"),
    size: int = Query(5, description="Number of top results")
):
    try:
        query = {
            "range": {
                "trip_date": {
                    "gte": date_gte,
                    "lte": date_lte
                }
            }
        }

        response = es.search(
            index=INDEX_NAME,
            size=size,
            query=query,
            sort=[{field: {"order": sort_order}}],
            source={
                "includes": [
                    "trip_summary.text",
                    "trip_date",
                    "driver",
                    "total_fare_inr"
                ]
            }
        )

        hits = response.get("hits", {}).get("hits", [])
        if not hits:
            return TripResponse(summary_text=f"No trips found for field `{field}`.", trips=[])

        trips = []
        summary_lines = []

        for h in hits:
            src = h["_source"]
            trip_date = src.get("trip_date")
            driver = src.get("driver")
            fare = src.get("total_fare_inr")
            trips.append(TripSummary(trip_date=trip_date, driver=driver, fare=round(fare, 2)))
            date_str = datetime.strptime(trip_date, "%Y-%m-%d").strftime("%d %b %Y")
            summary_lines.append(f"\u2022 On {date_str}, driven by {driver}, total fare ₹{fare:.2f}")

        summary_text = f"Top {size} trip(s) by `{field}` ({sort_order}):\n" + "\n".join(summary_lines)

        return TripResponse(summary_text=summary_text, trips=trips)

    except es_exceptions.ApiError as e:
        return JSONResponse(status_code=500, content={"summary_text": f"Elasticsearch error: {str(e)}", "trips": []})
    except Exception as e:
        return JSONResponse(status_code=500, content={"summary_text": f"Unexpected error: {str(e)}", "trips": []})


# ✅ NEW STATS ROUTES (to fix misrouting by Claude for 'total' queries)

@router.get("/stats/totalDistance")
def get_total_distance(
    date_gte: str = Query("2025-01-01"),
    date_lte: str = Query("2025-12-31")
):
    try:
        query = {
            "range": {
                "trip_date": {
                    "gte": date_gte,
                    "lte": date_lte
                }
            }
        }
        aggs = {"total_distance": {"sum": {"field": "distance_km"}}}

        response = es.search(index=INDEX_NAME, size=0, query=query, aggs=aggs)
        total_km = round(response["aggregations"]["total_distance"]["value"], 2)
        return {"total_distance_km": total_km}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.get("/stats/totalDuration")
def get_total_duration(
    date_gte: str = Query("2025-01-01"),
    date_lte: str = Query("2025-12-31")
):
    try:
        query = {"range": {"trip_date": {"gte": date_gte, "lte": date_lte}}}
        aggs = {"total_duration": {"sum": {"field": "duration_minutes"}}}

        response = es.search(index=INDEX_NAME, size=0, query=query, aggs=aggs)
        total_minutes = response["aggregations"]["total_duration"]["value"]
        total_hours = round(total_minutes / 60, 2)
        return {"total_duration_minutes": total_minutes, "total_duration_hours": total_hours}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.get("/stats/totalFare")
def get_total_fare(
    date_gte: str = Query("2025-01-01"),
    date_lte: str = Query("2025-12-31")
):
    try:
        query = {"range": {"trip_date": {"gte": date_gte, "lte": date_lte}}}
        aggs = {"total_fare": {"sum": {"field": "total_fare_inr"}}}

        response = es.search(index=INDEX_NAME, size=0, query=query, aggs=aggs)
        total = round(response["aggregations"]["total_fare"]["value"], 2)
        return {"total_fare_inr": total}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
