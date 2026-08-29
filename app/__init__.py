import os

from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

from config import config_by_name
from app.extensions import db, login_manager, csrf
from app.utils import setup_logging, logger


def create_app(config_name=None):
    config_name = config_name or os.environ.get("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    os.makedirs(os.path.join(app.instance_path), exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    setup_logging(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.events import events_bp
    from app.routes.profile import profile_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(profile_bp)

    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    @app.context_processor
    def inject_categories():
        from app.models import CATEGORIES

        return {"ALL_CATEGORIES": CATEGORIES}

    @app.template_global()
    def avatar_url(user):
        from flask import url_for

        if not user or not user.profile_image or user.profile_image == "default-avatar.svg":
            return url_for("static", filename="img/default-avatar.svg")
        return url_for("static", filename=f"uploads/{user.profile_image}")

    return app


def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        logger.error("Internal server error: %s", error)
        return render_template("errors/500.html"), 500

    @app.errorhandler(CSRFError)
    def csrf_error(error):
        return render_template("errors/403.html", reason=error.description), 400
