import pickle
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

_model = None


def load_model():
    model_path = Path(__file__).parent / "ride_predictor" / "model" / "model.pkl"
    logging.info("🔍 Looking for model at: %s", model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Model file missing at: {model_path}")
    logging.info("📁 Model exists: True")
    with open(model_path, "rb") as f:
        _model = pickle.load(f)
    logging.info("✅ Model loaded into memory")
    return _model


def predict_duration(payload, version, source="http"):
    logging.info("🎯 Running prediction...")

    model = load_model()  # Safe even if already loaded

    ride_id = int(payload.get("ride_id"))
    pu = int(payload.get("PULocationID"))
    do = int(payload.get("DOLocationID"))
    distance = float(payload.get("trip_distance"))

    sample = {
        "ride_id": ride_id,
        "PULocationID": pu,
        "DOLocationID": do,
        "trip_distance": distance,
    }

    prediction_value = model.predict([sample])[0]

    result = {
        "type": "prediction",
        "model": "ride_duration_prediction_model",
        "version": version,
        "source": source,
        "prediction": {"ride_id": ride_id, "ride_duration": float(prediction_value)},
    }

    print(f"💥 Emitted prediction event: {result}")
    return result, prediction_value
