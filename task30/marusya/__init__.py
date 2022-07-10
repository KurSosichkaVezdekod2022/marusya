import os

from flask import Flask

app = Flask(__name__)
app.config.from_object("marusya.config")

from random import choice
import marusya.routs

