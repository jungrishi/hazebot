import os
from logging.config import dictConfig


PG_DB = os.getenv("POSTGRES_DB", "postgres")
PG_HOST = os.getenv("POSTGRES_HOST", "db")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
PG_PORT = os.getenv("POSTGRES_POST", "5432")
PG_USER = os.getenv("POSTGRES_USER", "postgres")


# Init logging before doing anything else.
#
# TODO: Send errors to admins as emails
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

import flask
import flask_migrate
import flask_sqlalchemy
from airq import cache
from airq import middleware

app = flask.Flask(__name__)

# We have to use this `setattr` hack here or Mypy gets really confused.
# See https://github.com/python/mypy/issues/2427 for details.
setattr(app, "wsgi_app", middleware.LoggingMiddleware(app.wsgi_app))
if os.getenv("FLASK_ENV") == "development":
    setattr(
        app, "wsgi_app", middleware.ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    )

config = {
    "CACHE_TYPE": "memcached",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_MEMCACHED_SERVERS": os.getenv("MEMCACHED_SERVERS", "").split(","),
    "SQLALCHEMY_DATABASE_URI": f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
}
app.config.from_mapping(config)
cache.init(app)

db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)
