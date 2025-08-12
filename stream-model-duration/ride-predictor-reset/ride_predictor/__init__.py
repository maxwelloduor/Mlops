import os
import json
import logging

import azure.functions as func
from predictor import predict_duration

MODEL_VERSION = os.getenv("MODEL_VERSION", "Test123")


def main(req: func.HttpRequest, output_event: func.Out[str]) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        logging.info("Request JSON: %s", req_body)

        # Defensive: avoid feedback loop if someone posts a prediction event
        if isinstance(req_body, dict) and req_body.get("type") == "prediction":
            logging.warning(
                "Received a prediction-type payload; skipping to avoid feedback loop."
            )
            return func.HttpResponse(
                json.dumps({"message": "Skipping prediction-type payload"}),
                status_code=200,
                mimetype="application/json",
            )

        # Ensure required fields are present and normalize naming
        ride_id = req_body.get("ride_id")
        pu = req_body.get("PULocationID")
        do = req_body.get("DOLocationID")
        # Accept either "trip_distance" or legacy "distance"
        distance = req_body.get("trip_distance", req_body.get("distance"))

        if ride_id is None or pu is None or do is None or distance is None:
            missing = [
                k
                for k in ("ride_id", "PULocationID", "DOLocationID")
                if req_body.get(k) is None
            ]
            if req_body.get("trip_distance", None) is None:
                missing.append("trip_distance/distance")
            return func.HttpResponse(
                json.dumps({"error": f"Missing required fields: {missing}"}),
                status_code=400,
                mimetype="application/json",
            )

        # Build normalized payload for predictor
        normalized = {
            "ride_id": int(ride_id),
            "PULocationID": int(pu),
            "DOLocationID": int(do),
            "trip_distance": float(distance),
        }

        result_event, _ = predict_duration(
            normalized, version=MODEL_VERSION, source="http"
        )

        # Emit full prediction event
        output_event.set(json.dumps(result_event))
        logging.info("💥 Emitted prediction event: %s", result_event)

        return func.HttpResponse(
            json.dumps(result_event), status_code=200, mimetype="application/json"
        )

    except json.JSONDecodeError:
        logging.error("Could not parse JSON body", exc_info=True)
        return func.HttpResponse("Invalid JSON", status_code=400)
    except (ValueError, TypeError) as e:
        logging.error("Bad input for prediction: %s", e, exc_info=True)
        return func.HttpResponse(f"Invalid input: {e}", status_code=400)
