# Directory structure:
# src/
# ├── main.py
# ├── routers/
# │   ├── search.py
# │   ├── top_trips.py
# │   ├── locations.py
# │   └── stats.py
# ├── schemas/
# │   └── models.py
# ├── services/
# │   └── elasticsearch_queries.py
# └── utils/
#     └── es_client.py

# main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from pyngrok import ngrok, conf
import os
import nest_asyncio
import uvicorn

from routers import search, top_trips, locations, stats

load_dotenv()

# Environment variables
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")
ES_HOST = os.getenv("ES_HOST", "https://your-es-host")
ES_API_KEY = os.getenv("ELASTIC_API_KEY")
INDEX_NAME = os.getenv("INDEX_NAME", "notebook_index_semantic_v1")

# Setup ngrok
conf.get_default().auth_token = NGROK_AUTH_TOKEN
ngrok_tunnel = ngrok.connect(8000)
print("🚀 Public URL:", ngrok_tunnel.public_url)

# FastAPI app
app = FastAPI(
    title="Uber Trip Intelligence API",
    version="1.0.0",
    description="Query Uber trip data with semantic, metric, and aggregation-based queries"
)

# Routers
app.include_router(search.router)
app.include_router(top_trips.router)
app.include_router(locations.router)
app.include_router(stats.router)

# Run server
if __name__ == "__main__":
    nest_asyncio.apply()
    uvicorn.run(app, port=8000, host="0.0.0.0")
