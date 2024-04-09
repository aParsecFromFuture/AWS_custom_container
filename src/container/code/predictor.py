import io
import os
import json
import joblib
import pandas as pd

from common import feature_columns_names, label_column, columns_dtype

import flask
from flask import Response

# Predictor class to handle model predictions
class Predictor:
    model = None

    @classmethod
    def get_model(cls):
        model_path = os.path.join(os.environ.get("SM_MODEL_DIR"), "model.joblib")
        cls.model = joblib.load(model_path)
        return cls.model
        
    @classmethod
    def predict(cls, X):
        clf = cls.get_model()
        return clf.predict(X)


app = flask.Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    is_healthy = Predictor.get_model() is not None
    status = 200 if is_healthy else 404
    return flask.Response(
        response='\n', status=status, mimetype='application/json'
    )

# Endpoint to handle incoming requests
@app.route("/invocations", methods=["POST"])
def transformation():
    # Check if incoming data is in CSV format
    if flask.request.content_type == "text/csv":
        # Read the incoming CSV data
        data = flask.request.data.decode("utf-8")
        data = pd.read_csv(
            io.StringIO(data),
            header=None,
            names=[label_column] + feature_columns_names,
            dtype=columns_dtype
        )

        # Make predictions using the Predictor class
        predictions = Predictor.predict(data)

        # Prepare the response as CSV
        out = io.StringIO()
        pd.DataFrame({"results": predictions}).to_csv(out, header=False, index=False)
        result = out.getvalue()
        
        # Return the response with status 200
        return Response(
            response=result, status=200, mimetype="text/csv"
        )
    else:
        # Return an error response if data format is not supported
        return Response(
            response="This predictor only supports CSV data", status=415, mimetype="text/plain"
        )
