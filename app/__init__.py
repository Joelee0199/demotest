from flask import Flask, render_template

from app.config import Config
from app.extensions import db, login_manager
from app.routes import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    register_blueprints(app)
    _register_error_handlers(app)

    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    return app


def _register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error.html", title="403",
                               message="你没有权限执行此操作。"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", title="404",
                               message="页面不存在。"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("error.html", title="500",
                               message="服务器内部错误，请稍后再试。"), 500
