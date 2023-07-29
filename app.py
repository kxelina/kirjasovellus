from flask import Flask
from os import getenv

app = Flask(__name__)

app.secret_key = getenv("SECRET_KEY")

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
import routes  