# type: ignore

from flask import Flask, jsonify

from app.common.error_handler import register_error_handlers
from app.permissions import permission_bp
from app.roles import role_bp

app = Flask(__name__)
register_error_handlers(app)
app.register_blueprint(role_bp)
app.register_blueprint(permission_bp)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""

    return jsonify({"status": "ok"})
