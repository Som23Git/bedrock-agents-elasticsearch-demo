# lambda_handler_bedrock_final.py
import logging
import requests
from typing import Dict, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Replace with your actual ngrok URL
NGROK_URL = "https://a5a8c9cf5a13.ngrok-free.app" 

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        logger.info("📥 Received event:")
        logger.info(event)

        action_group = event.get("actionGroup", "unknown")
        api_path = event.get("apiPath", "/")
        http_method = event.get("httpMethod", "GET").upper()
        parameters = event.get("parameters", [])
        message_version = event.get("messageVersion", "1.0")

        # Build full URL
        url = f"{NGROK_URL}{api_path}"
        query_params = {}
        headers = {
            "ngrok-skip-browser-warning": "true",
            "Content-Type": "application/json"
        }

        for param in parameters:
            name = param.get("name")
            value = param.get("value")
            if name:
                query_params[name] = value

        logger.info(f"🔀 Forwarding request to: {url}")
        logger.info(f"➡️ Method: {http_method}")
        logger.info(f"➡️ Query: {query_params}")

        # Make the request
        if http_method == "GET":
            resp = requests.get(url, params=query_params, headers=headers, timeout=10)
        elif http_method == "POST":
            body = event.get("requestBody", {})
            resp = requests.post(url, params=query_params, headers=headers, json=body, timeout=10)
        else:
            raise ValueError(f"❌ Unsupported HTTP method: {http_method}")

        resp.raise_for_status()
        logger.info(f"✅ Response from FastAPI: {resp.text}")

        # Extract natural language summary if available
        response_body = resp.json()
        if isinstance(response_body, dict) and "summary_text" in response_body:
            final_text = response_body["summary_text"]
        else:
            final_text = str(response_body)

        return {
            "messageVersion": message_version,
            "response": {
                "actionGroup": action_group,
                "apiPath": api_path,
                "httpMethod": http_method,
                "httpStatusCode": resp.status_code,
                "responseBody": {
                    "application/json": {
                        "body": {
                            "text": final_text
                        }
                    }
                }
            }
        }

    except Exception as e:
        logger.exception("❌ Lambda proxy failed")
        return {
            "messageVersion": event.get("messageVersion", "1.0"),
            "response": {
                "actionGroup": event.get("actionGroup", "unknown"),
                "apiPath": event.get("apiPath", "unknown"),
                "httpMethod": event.get("httpMethod", "GET"),
                "httpStatusCode": 500,
                "responseBody": {
                    "application/json": {
                        "body": {
                            "error": str(e)
                        }
                    }
                }
            }
        }