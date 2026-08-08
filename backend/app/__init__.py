# type: ignore

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""

    return jsonify({"status": "ok"})
