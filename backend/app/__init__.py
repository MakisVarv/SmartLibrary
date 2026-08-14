# type: ignore

from flask import Flask, jsonify

from app.auth.routes import auth_bp
from app.authors import author_bp
from app.books import book_bp
from app.categories import category_bp
from app.common.error_handler import register_error_handlers
from app.config import JWT_SECRET_KEY
from app.extensions import jwt
from app.permissions import permission_bp
from app.roles import role_bp
from app.users import user_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

jwt.init_app(app)
register_error_handlers(app)
app.register_blueprint(role_bp)
app.register_blueprint(permission_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(author_bp)
app.register_blueprint(category_bp)
app.register_blueprint(book_bp)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""

    return jsonify({"status": "ok"})
