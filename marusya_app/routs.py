import json
from flask import request
from . import app


@app.route("/", methods=["GET", "POST"])
def index():
    return ""
