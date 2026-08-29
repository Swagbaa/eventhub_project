import os

from sqlalchemy.pool import StaticPool

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration shared by every environment."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "instance", "eventhub.db")
    )
    # Some hosts (e.g. Render/Heroku) hand out "postgres://" — SQLAlchemy 1.4+/2.x needs "postgresql://"
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024  # 4 MB max upload

    OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
    OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

    LOG_FILE = os.path.join(basedir, "logs", "eventhub.log")

    EVENTS_PER_PAGE = 9


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # Keep a single shared in-memory connection alive for the whole test session,
    # otherwise every new connection would see a blank, table-less database.
    SQLALCHEMY_ENGINE_OPTIONS = {
        "poolclass": StaticPool,
        "connect_args": {"check_same_thread": False},
    }
    WTF_CSRF_ENABLED = False
    LOG_FILE = os.path.join(basedir, "logs", "eventhub-test.log")


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
