from flask import Flask, jsonify
import datetime

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "timestamp": datetime.datetime.utcnow().isoformat()
    })


@app.route("/")
def hello():
    return jsonify({
        "message": "Hello from my DevOps app!"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
