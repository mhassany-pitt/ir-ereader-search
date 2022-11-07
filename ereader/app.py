import os
from os.path import join, dirname
from apps.ereader import ereader
from apps.search import search
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), '.env'))

app = Flask(__name__)

CORS(app)

app.register_blueprint(ereader)
app.register_blueprint(search)
