from apps.ereader import ereader
from apps.search import search
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

app.config['storage-path'] = './storage'
app.config['courses-path'] = '{}/courses'.format(app.config['storage-path'])

CORS(app)

app.register_blueprint(ereader)
app.register_blueprint(search)
