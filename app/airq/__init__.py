from airq import config  # Do this first, it initializes everything
from airq.celery import celery  # This is necesary to start celery

from airq import api
from airq import management


app = config.app

# Register management commands
app.cli.command("sync")(management.sync)

# Register routes
app.route("/", methods=["GET"])(api.healthcheck)
app.route("/sms", methods=["POST"])(api.sms_reply)
app.route("/quality", methods=["GET"])(api.quality)
# REMOVE
app.route("/blowup", methods=["GET"])(api.remove_me)
