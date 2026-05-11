from app.routes.auth import auth_bp
from app.routes.posts import posts_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
