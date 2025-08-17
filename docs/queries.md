```
GET notebook_index_semantic_v1/_mapping
```
```
GET notebook_index_semantic_v1/_search
{
  "knn": {
    "field": "trip_summary.inference.chunks.embeddings",
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "bedrock-embeddings",
        "model_text": "last 5 trips in the year 2025"
      }
    },
    "k": 2,
    "num_candidates": 10
  },
  "query": {
    "bool": {
      "filter": {
        "range": {
          "trip_date": {
            "gte": "2025-01-01",
            "lte": "2025-12-31"
          }
        }
      }
    }
  },
  "_source": {
    "includes": ["trip_summary.text","distance_km","driver","duration_minutes","promotion_inr","total_fare_inr","trip_charge_inr","trip_date"]
  }
}
```

```
# last 5 trips in the year 2025
GET notebook_index_semantic_v1/_search
{
  "knn": {
    "field": "trip_summary.inference.chunks.embeddings",
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "bedrock-embeddings",
        "model_text": "last 5 trips in the year 2025"
      }
    },
    "k": 2,
    "num_candidates": 10
  },
  "query": {
    "bool": {
      "filter": {
        "range": {
          "trip_date": {
            "gte": "2025-01-01",
            "lte": "2025-12-31"
          }
        }
      }
    }
  },
  "sort": [
    {
      "trip_date": {
        "order": "desc"
      }
    }
  ],
  "_source": {
    "includes": [
      "trip_summary.text",
      "distance_km",
      "driver",
      "duration_minutes",
      "promotion_inr",
      "total_fare_inr",
      "trip_charge_inr",
      "trip_date"
    ]
  }
}
```

```
### what is the expensive trip that I had?
GET notebook_index_semantic_v1/_search
{
"size": 10,
"query": {
    "range": {
        "trip_date": {
            "gte": "2025-01-01",
            "lte": "2025-12-01"
        }
    }
},
"_source": {
    "includes": [
      "trip_summary.text",
      "distance_km",
      "driver",
      "duration_minutes",
      "promotion_inr",
      "total_fare_inr",
      "trip_charge_inr",
      "trip_date"
    ]
  },
"aggs": {
    "total_spent": {
        "sum": {
            "field": "total_fare_inr"
        }
    }
 },
 "sort": [
    {
      "total_fare_inr": {
        "order": "desc"
      }
    }
  ]
}
```

```
### what is the longest trip that I had in 2025?
GET notebook_index_semantic_v1/_search
{
"size": 10,
"query": {
    "range": {
        "trip_date": {
            "gte": "2025-01-01",
            "lte": "2025-12-01"
        }
    }
},
"_source": {
    "includes": [
      "trip_summary.text",
      "distance_km",
      "driver",
      "duration_minutes",
      "promotion_inr",
      "total_fare_inr",
      "trip_charge_inr",
      "trip_date"
    ]
  },
"aggs": {
    "total_travel_time": {
        "sum": {
            "field": "duration_minutes"
        }
    }
 },
 "sort": [
    {
      "duration_minutes": {
        "order": "desc"
      }
    }
  ]
}
```

```
### what is the shortest trip that I had in 2025?
GET notebook_index_semantic_v1/_search
{
"size": 10,
"query": {
    "range": {
        "trip_date": {
            "gte": "2025-01-01",
            "lte": "2025-12-01"
        }
    }
},
"_source": {
    "includes": [
      "trip_summary.text",
      "distance_km",
      "driver",
      "duration_minutes",
      "promotion_inr",
      "total_fare_inr",
      "trip_charge_inr",
      "trip_date"
    ]
  },
"aggs": {
    "total_travel_time": {
        "sum": {
            "field": "duration_minutes"
        }
    }
 },
 "sort": [
    {
      "duration_minutes": {
        "order": "asc"
      }
    }
  ]
}
```

```
### what is the longest trip that I had in 2024?
GET notebook_index_semantic_v1/_search
{
"size": 10,
"query": {
    "range": {
        "trip_date": {
            "gte": "2024-01-01",
            "lte": "2024-12-01"
        }
    }
},
"_source": {
    "includes": [
      "trip_summary.text",
      "distance_km",
      "driver",
      "duration_minutes",
      "promotion_inr",
      "total_fare_inr",
      "trip_charge_inr",
      "trip_date"
    ]
  },
"aggs": {
    "total_travel_time": {
        "sum": {
            "field": "duration_minutes"
        }
    }
 },
 "sort": [
    {
      "duration_minutes": {
        "order": "desc"
      }
    }
  ]
}
```

```
### what is the shortest trip that I had in 2024 and total travel time?
GET notebook_index_semantic_v1/_search
{
"size": 10,
"query": {
    "range": {
        "trip_date": {
            "gte": "2024-01-01",
            "lte": "2024-12-01"
        }
    }
},
"_source": {
    "includes": [
      "trip_summary.text",
      "distance_km",
      "driver",
      "duration_minutes",
      "promotion_inr",
      "total_fare_inr",
      "trip_charge_inr",
      "trip_date"
    ]
  },
"aggs": {
    "total_travel_time": {
        "sum": {
            "field": "duration_minutes"
        }
    }
 },
 "sort": [
    {
      "duration_minutes": {
        "order": "asc"
      }
    }
  ]
}
```

```
### what is the highest promotion trip that I had in 2025?
GET notebook_index_semantic_v1/_search
{
"size": 10,
"query": {
    "range": {
        "trip_date": {
            "gte": "2024-01-01",
            "lte": "2024-12-01"
        }
    }
},
"_source": {
    "includes": [
      "trip_summary.text",
      "distance_km",
      "driver",
      "duration_minutes",
      "promotion_inr",
      "total_fare_inr",
      "trip_charge_inr",
      "trip_date"
    ]
  },
"aggs": {
    "total_promotion_inr": {
        "sum": {
            "field": "promotion_inr"
        }
    }
 },
 "sort": [
    {
      "promotion_inr": {
        "order": "asc"
      }
    }
  ]
}
```
```
### what is the lowest promotion trip that I had in 2025?
GET notebook_index_semantic_v1/_search
{
"size": 10,
"query": {
    "range": {
        "trip_date": {
            "gte": "2024-01-01",
            "lte": "2024-12-01"
        }
    }
},
"_source": {
    "includes": [
      "trip_summary.text",
      "distance_km",
      "driver",
      "duration_minutes",
      "promotion_inr",
      "total_fare_inr",
      "trip_charge_inr",
      "trip_date"
    ]
  },
"aggs": {
    "total_promotion_inr": {
        "sum": {
            "field": "promotion_inr"
        }
    }
 },
 "sort": [
    {
      "promotion_inr": {
        "order": "desc"
      }
    }
  ]
}
```

```
### what is the highest fare trip that I had in 2025 and total spend?
GET notebook_index_semantic_v1/_search
{
"size": 10,
"query": {
    "range": {
        "trip_date": {
            "gte": "2025-01-01",
            "lte": "2025-12-01"
        }
    }
},
"_source": {
    "includes": [
      "trip_summary.text",
      "distance_km",
      "driver",
      "duration_minutes",
      "promotion_inr",
      "total_fare_inr",
      "trip_charge_inr",
      "trip_date"
    ]
  },
"aggs": {
    "total_spend": {
        "sum": {
            "field": "trip_charge_inr"
        }
    }
 },
 "sort": [
    {
      "trip_charge_inr": {
        "order": "desc"
      }
    }
  ]
}
```

```
### what is the highest fare trip that I had in 2024 and total spend?
GET notebook_index_semantic_v1/_search
{
"size": 10,
"query": {
    "range": {
        "trip_date": {
            "gte": "2024-01-01",
            "lte": "2024-12-01"
        }
    }
},
"_source": {
    "includes": [
      "trip_summary.text",
      "distance_km",
      "driver",
      "duration_minutes",
      "promotion_inr",
      "total_fare_inr",
      "trip_charge_inr",
      "trip_date"
    ]
  },
"aggs": {
    "total_spend": {
        "sum": {
            "field": "trip_charge_inr"
        }
    }
 },
 "sort": [
    {
      "trip_charge_inr": {
        "order": "desc"
      }
    }
  ]
}
```

```
### what is the shortest trip distance that I had in 2024 and total distance covered?
GET notebook_index_semantic_v1/_search
{
"size": 10,
"query": {
    "range": {
        "trip_date": {
            "gte": "2024-01-01",
            "lte": "2024-12-01"
        }
    }
},
"_source": {
    "includes": [
      "trip_summary.text",
      "distance_km",
      "driver",
      "duration_minutes",
      "promotion_inr",
      "total_fare_inr",
      "trip_charge_inr",
      "trip_date"
    ]
  },
"aggs": {
    "total_travel_distance": {
        "sum": {
            "field": "distance_km"
        }
    }
 },
 "sort": [
    {
      "distance_km": {
        "order": "asc"
      }
    }
  ]
}
```

```
### what is the shortest trip distance that I had in 2025 and total distance covered?
GET notebook_index_semantic_v1/_search
{
"size": 10,
"query": {
    "range": {
        "trip_date": {
            "gte": "2025-01-01",
            "lte": "2025-12-01"
        }
    }
},
"_source": {
    "includes": [
      "trip_summary.text",
      "distance_km",
      "driver",
      "duration_minutes",
      "promotion_inr",
      "total_fare_inr",
      "trip_charge_inr",
      "trip_date"
    ]
  },
"aggs": {
    "total_travel_distance": {
        "sum": {
            "field": "distance_km"
        }
    }
 },
 "sort": [
    {
      "distance_km": {
        "order": "asc"
      }
    }
  ]
}
```
```
### what is the longest trip distance that I had in 2024?
GET notebook_index_semantic_v1/_search
{
"size": 10,
"query": {
    "range": {
        "trip_date": {
            "gte": "2024-01-01",
            "lte": "2024-12-01"
        }
    }
},
"_source": {
    "includes": [
      "trip_summary.text",
      "distance_km",
      "driver",
      "duration_minutes",
      "promotion_inr",
      "total_fare_inr",
      "trip_charge_inr",
      "trip_date"
    ]
  },
"aggs": {
    "total_travel_distance": {
        "sum": {
            "field": "distance_km"
        }
    }
 },
 "sort": [
    {
      "distance_km": {
        "order": "desc"
      }
    }
  ]
}
```
```
# In 2025, what is the most frequent pickup location, by month?
GET notebook_index_semantic_v1/_search
{
  "size": 0,
  "query": {
    "range": {
      "trip_date": {
        "gte": "2025-01-01",
        "lte": "2025-12-31"
      }
    }
  },
  "aggs": {
    "by_month": {
      "date_histogram": {
        "field": "trip_date",
        "calendar_interval": "month"
      },
      "aggs": {
        "top_locations": {
          "terms": {
            "field": "pickup_location.keyword",
            "size": 1
          }
        }
      }
    }
  }
}
```
```
# In 2025, what is the most frequent pickup location in total in the year 2025?
GET notebook_index_semantic_v1/_search
{
  "size": 0,
  "query": {
    "range": {
      "trip_date": {
        "gte": "2025-01-01",
        "lte": "2025-12-31"
      }
    }
  },
  "aggs": {
    "top_pickup_locations": {
      "terms": {
        "field": "pickup_location.keyword",
        "size": 5
      }
    }
  }
}
```
```
# In 2025, what is the most frequent drop location in total?
GET notebook_index_semantic_v1/_search
{
  "size": 0,
  "query": {
    "range": {
      "trip_date": {
        "gte": "2025-01-01",
        "lte": "2025-12-31"
      }
    }
  },
  "aggs": {
    "top_drop_locations": {
      "terms": {
        "field": "dropoff_location.keyword",
        "size": 5
      }
    }
  }
}
```
```
## What is the most times I have taken the trip in 2025 in a single day?
GET notebook_index_semantic_v1/_search
{
  "size": 0,
  "query": {
    "range": {
      "trip_date": {
        "gte": "2025-01-01",
        "lte": "2025-12-31"
      }
    }
  },
  "aggs": {
    "most_trips_day": {
      "terms": {
        "field": "trip_date",
        "size": 1,
        "order": {
          "_count": "desc"
        }
      }
    }
  }
}
```
```
## What is the most times I have taken the trip in 2024 in a single day?
GET notebook_index_semantic_v1/_search
{
  "size": 0,
  "query": {
    "range": {
      "trip_date": {
        "gte": "2024-01-01",
        "lte": "2024-12-31"
      }
    }
  },
  "aggs": {
    "most_trips_day": {
      "terms": {
        "field": "trip_date",
        "size": 1,
        "order": {
          "_count": "desc"
        }
      }
    }
  }
}
```
```
### What is the most frequent HH:MM that I travelled in trips in UTC timestamp?
GET notebook_index_semantic_v1/_search
{
  "size": 0,
  "aggs": {
    "pickup_hours": {
      "terms": {
        "script": {
          "source": "doc['pickup_timestamp'].value.getHour()",
          "lang": "painless"
        },
        "size": 24,
        "order": {
          "_count": "desc"
        }
      }
    }
  }
}
```
```
### What is the most frequent HH:MM that I travelled in trips in IST timestamp?
GET notebook_index_semantic_v1/_search
{
  "size": 0,
  "aggs": {
    "pickup_hours_ist": {
      "terms": {
        "script": {
          "source": """
            ZonedDateTime istTime = doc['pickup_timestamp'].value.plusHours(5).plusMinutes(30);
            return istTime.getHour();
          """,
          "lang": "painless"
        },
        "size": 24,
        "order": {
          "_count": "desc"
        }
      }
    }
  }
}
```
```
### Drilling down further to 30 minutes
GET notebook_index_semantic_v1/_search
{
  "size": 0,
  "aggs": {
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
        "order": {
          "_count": "desc"
        }
      }
    }
  }
}
```
```
### Around the travel hours, what is the average/max/min/median fare
GET notebook_index_semantic_v1/_search
{
  "size": 0,
  "aggs": {
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
        "order": {
          "_count": "desc"
        }
      },
      "aggs": {
        "avg_fare": {
          "avg": {
            "field": "total_fare_inr"
          }
        },
        "max_fare": {
          "max": {
            "field": "total_fare_inr"
          }
        },
        "min_fare": {
          "min": {
            "field": "total_fare_inr"
          }
        },
        "percentiles_fare": {
          "percentiles": {
            "field": "total_fare_inr",
            "percents": [50.0]
          }
        }
      }
    }
  }
}
```
```
GET notebook_index_semantic_v1/_search
{
  "profile": true,
  "size": 5,
  "knn": {
    "field": "trip_summary.inference.chunks.embeddings",
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "bedrock-embeddings",
        "model_text": "last 5 trips in the year 2025"
      }
    },
    "k": 2,
    "num_candidates": 10
  },
  "query": {
    "bool": {
      "filter": {
        "range": {
          "trip_date": {
            "gte": "2025-01-01",
            "lte": "2025-12-31"
          }
        }
      }
    }
  },
  "_source": {
    "includes": ["trip_summary.text","distance_km","driver","duration_minutes","promotion_inr","total_fare_inr","trip_charge_inr","trip_date"]
  },
  "sort": [
    {
      "trip_date": {
        "order": "desc"
      }
    }
  ]
}
```
```
#List all trips with selected fields
POST /_query
{
  "query": """
    FROM notebook_index_basic_v1
    | KEEP trip_date, driver, total_fare_inr
    | SORT trip_date DESC
    | LIMIT 10
  """
}
```
```
#### ESQL - https://www.elastic.co/docs/solutions/search/esql-search-tutorial
#Highest fare trip
POST /_query
{
  "profile": true,
  "query": """
    FROM notebook_index_basic_v1
    | SORT total_fare_inr DESC
    | LIMIT 1
  """
}
```