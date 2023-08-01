from flask import Flask
from os import getenv

app = Flask(__name__)

app.secret_key = getenv("SECRET_KEY")

UPLOAD_FOLDER = "static/images/upload"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

PROFILE_FOLDER = "static/images/profile"
app.config["PROFILE_FOLDER"] = PROFILE_FOLDER
import routes  