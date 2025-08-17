# utils/es_client.py
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

ES_HOST = os.getenv("ES_HOST", "https://your-es-host")
ES_API_KEY = os.getenv("ELASTIC_API_KEY")

es = Elasticsearch(
    hosts=[ES_HOST],
    api_key=ES_API_KEY,
    request_timeout=30,
    retry_on_timeout=True,
    max_retries=3
)

__all__ = ["es"]
