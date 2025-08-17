# routers/locations.py
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from elasticsearch import exceptions as es_exceptions
from utils.es_client import es
import os

router = APIRouter(prefix="/locations", tags=["Frequent Locations"])

INDEX_NAME = os.getenv("INDEX_NAME", "notebook_index_semantic_v1")

@router.get("/pickup/top")
def most_frequent_pickup(
    size: int = Query(5, description="Top N locations to return"),
    year: str = Query("2025", description="Year to filter trips")
):
    try:
        response = es.search(
            index=INDEX_NAME,
            size=0,
            query={
                "range": {
                    "trip_date": {
                        "gte": f"{year}-01-01",
                        "lte": f"{year}-12-31"
                    }
                }
            },
            aggs={
                "top_pickup_locations": {
                    "terms": {
                        "field": "pickup_location.keyword",
                        "size": size
                    }
                }
            }
        )
        buckets = response["aggregations"]["top_pickup_locations"]["buckets"]
        locations = [f"{b['key']} ({b['doc_count']} trips)" for b in buckets]
        return {"top_pickup_locations": locations}

    except es_exceptions.ApiError as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/dropoff/top")
def most_frequent_dropoff(
    size: int = Query(5, description="Top N locations to return"),
    year: str = Query("2025", description="Year to filter trips")
):
    try:
        response = es.search(
            index=INDEX_NAME,
            size=0,
            query={
                "range": {
                    "trip_date": {
                        "gte": f"{year}-01-01",
                        "lte": f"{year}-12-31"
                    }
                }
            },
            aggs={
                "top_drop_locations": {
                    "terms": {
                        "field": "dropoff_location.keyword",
                        "size": size
                    }
                }
            }
        )
        buckets = response["aggregations"]["top_drop_locations"]["buckets"]
        locations = [f"{b['key']} ({b['doc_count']} trips)" for b in buckets]
        return {"top_dropoff_locations": locations}

    except es_exceptions.ApiError as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
