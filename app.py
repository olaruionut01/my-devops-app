from flask import Flask, jsonify
import datetime
import os
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

LOG_LEVEL = os.environ.get("LOG_LEVEL", "info")
APP_ENV   = os.environ.get("APP_ENV", "development")
API_KEY   = os.environ.get("API_KEY", "")


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "timestamp": datetime.datetime.utcnow().isoformat()
    })


@app.route("/hello")
def hello():
    return jsonify({
        "message": "Hello from my DevOps app!"
    })


@app.route("/secret-check")
def secret_check():
    return jsonify({"api_key_set": bool(API_KEY)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
