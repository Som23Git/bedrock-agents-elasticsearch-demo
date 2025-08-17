# routers/stats.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from elasticsearch import exceptions as es_exceptions
from utils.es_client import es
import os

router = APIRouter(prefix="/stats", tags=["Time-based Stats"])

INDEX_NAME = os.getenv("INDEX_NAME", "notebook_index_semantic_v1")

@router.get("/frequentTimeIST")
def most_frequent_half_hour():
    try:
        response = es.search(
            index=INDEX_NAME,
            size=0,
            aggs={
                "pickup_30min_ist": {
                    "terms": {
                        "script": {
                            "source": """
                                ZonedDateTime ist = doc['pickup_timestamp'].value.plusHours(5).plusMinutes(30);
                                int hour = ist.getHour();
                                int minute = ist.getMinute();
                                int roundedMinute = minute < 30 ? 0 : 30;
                                String hourStr = hour < 10 ? "0" + hour : "" + hour;
                                String minStr = roundedMinute == 0 ? "00" : "30";
                                return hourStr + ":" + minStr;
                            """,
                            "lang": "painless"
                        },
                        "size": 48,
                        "order": {"_count": "desc"}
                    }
                }
            }
        )
        buckets = response["aggregations"]["pickup_30min_ist"]["buckets"]
        intervals = [f"{b['key']} ({b['doc_count']} trips)" for b in buckets]
        return {"frequent_intervals_IST": intervals}

    except es_exceptions.ApiError as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/fareStatsByTimeIST")
def fare_stats_by_half_hour():
    try:
        response = es.search(
            index=INDEX_NAME,
            size=0,
            aggs={
                "pickup_30min_ist": {
                    "terms": {
                        "script": {
                            "source": """
                                ZonedDateTime ist = doc['pickup_timestamp'].value.plusHours(5).plusMinutes(30);
                                int hour = ist.getHour();
                                int minute = ist.getMinute();
                                int roundedMinute = minute < 30 ? 0 : 30;
                                String hourStr = hour < 10 ? "0" + hour : "" + hour;
                                String minStr = roundedMinute == 0 ? "00" : "30";
                                return hourStr + ":" + minStr;
                            """,
                            "lang": "painless"
                        },
                        "size": 48
                    },
                    "aggs": {
                        "avg_fare": {"avg": {"field": "total_fare_inr"}},
                        "max_fare": {"max": {"field": "total_fare_inr"}},
                        "min_fare": {"min": {"field": "total_fare_inr"}},
                        "median_fare": {
                            "percentiles": {
                                "field": "total_fare_inr",
                                "percents": [50.0]
                            }
                        }
                    }
                }
            }
        )

        results = []
        for b in response["aggregations"]["pickup_30min_ist"]["buckets"]:
            results.append({
                "interval": b["key"],
                "avg_fare": round(b["avg_fare"]["value"], 2) if b["avg_fare"]["value"] else None,
                "max_fare": b["max_fare"]["value"],
                "min_fare": b["min_fare"]["value"],
                "median_fare": b["median_fare"]["values"]["50.0"]
            })

        return {"fare_stats_by_half_hour_IST": results}

    except es_exceptions.ApiError as e:
        return JSONResponse(status_code=500, content={"error": str(e)})