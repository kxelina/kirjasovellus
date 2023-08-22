from os import getenv
from flask import Flask

app = Flask(__name__)

app.secret_key = getenv("SECRET_KEY")

UPLOAD_FOLDER = "static/images/upload"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

PROFILE_FOLDER = "static/images/profile"
app.config["PROFILE_FOLDER"] = PROFILE_FOLDER

BOOK_FOLDER = "static/images/book_pic"
app.config["BOOK_FOLDER"] = BOOK_FOLDER
import routes
