import os
import io
from PIL import Image
from flask import abort, request, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from db import db
import book


def login(username, password):
    sql = text("SELECT password, id FROM users WHERE username = :username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if not user or not check_password_hash(user[0], password):
        return False

    session["user_id"] = user[1]
    session["username"] = username
    session["csrf_token"] = os.urandom(16).hex()
    return True


def logout():
    keys_to_remove = ["user_id", "username", "csrf_token"]
    for key in keys_to_remove:
        session.pop(key, None)


def create_new_user(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text(
            "INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
        book.add_folders("want-to-read", username)
        book.add_folders("currently-reading", username)
        book.add_folders("read", username)
        book.add_folders("dropped", username)
    except Exception as error:
        print("The error is: ", error)
        return False

    return login(username, password)


def update_user_info(user_id, new_password):
    hash_value = generate_password_hash(new_password)
    try:
        sql = text(
            "UPDATE users SET password = :new_password WHERE id = :user_id")
        db.session.execute(
            sql, {"new_password": hash_value, "user_id": user_id})
        db.session.commit()
    except Exception as error:
        print("Error updating user info:", error)


def get_user_id():
    return session.get("user_id", 0)


def check_csrf():
    csrf_token = session.get("csrf_token")
    form_csrf_token = request.form.get("csrf_token")
    if csrf_token != form_csrf_token:
        abort(403)


def check_csrf_token():
    csrf_token = session.get("csrf_token")
    if csrf_token is None:
        abort(403)


def upload_user_icon(filename):
    user_name = session.get("username")
    file_name, file_extension = os.path.splitext(filename)
    sql = text(
        '''INSERT INTO images (user_icon, username, file_extension)
        VALUES (:user_icon_data, :username, :file_extension) ON CONFLICT (username)
        DO UPDATE SET file_extension = :file_extension, user_icon = :user_icon_data''')
    try:
        image = book.read_image_from_path(filename)
    except Exception as error:
        print(error)
        return False
    db.session.execute(sql, {"user_icon_data": image,
                       "username": user_name, "file_extension": file_extension})
    db.session.commit()
    return True


def get_user_icon():
    user_name = session.get("username")
    sql = text(
        "SELECT user_icon, file_extension FROM images WHERE username = :username")
    result = db.session.execute(sql, {"username": user_name})
    file_data = result.fetchone()

    if file_data is None:
        filename = "static/images/default-profile.jpg"
    else:
        filename = os.path.join(
            app.config["PROFILE_FOLDER"], user_name + file_data[1])
        image_data = io.BytesIO(file_data[0])

        image = Image.open(image_data)
        image.save(filename)
    return filename
