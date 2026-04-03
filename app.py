from flask import Flask, jsonify, request
import datetime
import os
from prometheus_flask_exporter import PrometheusMetrics
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Build DB URL from environment variables
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "appdb")
DB_USER = os.environ.get("DB_USER", "appuser")
DB_PASS = os.environ.get("DB_PASSWORD", "apppassword")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "info")
APP_ENV = os.environ.get("APP_ENV", "development")
API_KEY = os.environ.get("API_KEY", "")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Simple model — one table, two columns
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}


# Create tables on startup
if not app.config.get("TESTING"):
    with app.app_context():
        db.create_all()


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "env": APP_ENV,
        "timestamp": datetime.datetime.utcnow().isoformat()
    })


@app.route("/hello")
def hello():
    return jsonify({
        "message": "Hello from v2!",
        "log_level": LOG_LEVEL
    })


@app.route("/secret-check")
def secret_check():
    return jsonify({"api_key_set": bool(API_KEY)})


@app.route("/items", methods=["GET"])
def get_items():
    items = Item.query.all()
    return jsonify([i.to_dict() for i in items])


@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json(silent=True)

    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400
    item = Item(name=data["name"])
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
