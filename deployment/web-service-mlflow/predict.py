import os
import pickle

import mlflow
from flask import Flask, request, jsonify


RUN_ID = os.getenv('RUN_ID', '1535527ff96f404dbe2ffac68769a7e3')


logged_model = "wasbs://mlflow-artifacts-remote@mlflowartifactsstore.blob.core.windows.net/e2e7b52ffac646a089a0793f1f38875b/artifacts/model"
model = mlflow.pyfunc.load_model(logged_model)

mlflow.sklearn.log_model(model, artifact_path="model")


def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features


def predict(features):
    preds = model.predict(features)
    return float(preds[0])


app = Flask('duration-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)

    result = {
        'duration': pred,
        'model_version': RUN_ID
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
