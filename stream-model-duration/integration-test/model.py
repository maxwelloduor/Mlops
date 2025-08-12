# inside model.py
import json
import base64


class ModelService:
    def __init__(self, model, model_version='test'):
        self.model = model
        self.model_version = model_version

    def prepare_features(self, ride):
        return {
            "PU_DO": f"{ride['PULocationID']}_{ride['DOLocationID']}",
            "trip_distance": ride["trip_distance"],
        }

    def predict(self, features):
        preds = self.model.predict([features])
        return preds[0]

    def lambda_handler(self, event):
        predictions = []
        for record in event["Records"]:
            data = base64_decode(record["kinesis"]["data"])
            features = self.prepare_features(data["ride"])
            duration = self.predict(features)
            predictions.append(
                {
                    "model": "ride_duration_prediction_model",
                    "version": self.model_version,
                    "prediction": {
                        "ride_duration": duration,
                        "ride_id": data["ride_id"],
                    },
                }
            )
        return {"predictions": predictions}


def base64_decode(encoded):
    payload = base64.b64decode(encoded)
    return json.loads(payload)
