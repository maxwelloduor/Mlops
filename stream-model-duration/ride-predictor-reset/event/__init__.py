import os
import json
import logging
from unittest import result

import azure.functions as func
from predictor import predict_duration

MODEL_VERSION = os.getenv("MODEL_VERSION", "Test123")


def main(event: func.EventHubEvent, output_event: func.Out[str]) -> None:
    try:
        payload = event.get_body().decode("utf-8")
        payload = json.loads(payload)

        logging.info("✅ Received Event Hub message: %s", payload)

        # Skip prediction if message already contains prediction (feedback loop)
        if isinstance(payload, dict) and payload.get("type") == "prediction":
            logging.info("⚠️ Skipping prediction event to avoid feedback loop.")
            return
        logging.info("🔍 Starting prediction flow...")

        result_event, _ = predict_duration(
            payload, version=MODEL_VERSION, source="event"
        )

        output_event.set(json.dumps(result_event))

    except ValueError as ve:
        logging.error("Invalid value in prediction input: %s", ve, exc_info=True)
    except TypeError as te:
        logging.error("Type mismatch error: %s", te, exc_info=True)
    except RuntimeError as re:
        logging.error("Runtime error during prediction: %s", re, exc_info=True)
