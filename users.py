import os
import psycopg2
from db import db
from flask import abort, request, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

def login(name, password):
    sql = text("SELECT password, id FROM users WHERE name = :name")
    result = db.session.execute(sql, {"name": name})
    user = result.fetchone()

    if not user or not check_password_hash(user[0], password):
        return False

    session["user_id"] = user[1]
    session["username"] = name
    session["csrf_token"] = os.urandom(16).hex()

    return True

def logout():
    keys_to_remove = ["user_id", "username", "csrf_token"]
    for key in keys_to_remove:
        session.pop(key, None)

def create_new_user(name, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (name, password) VALUES (:name, :password)")
        db.session.execute(sql, {"name": name, "password": hash_value})
        db.session.commit()
        print("HELLO")
    except Exception as e:
       # By this way we can know about the type of error occurring
        print("The error is: ",e)
        return False

    return True

def user_id():
    return session.get("user_id", 0)

def check_csrf():
    csrf_token = session.get("csrf_token")
    form_csrf_token = request.form.get("csrf_token")
    if csrf_token != form_csrf_token:
        abort(403)

def save_image_to_database(image_path):
    with open(image_path, 'rb') as file:
        image_data = file.read()
    return psycopg2.Binary(image_data)

# def upload_all(filename):
#     sql = "INSERT INTO images (user_icon, folder_pic, book_pic) VALUES (?, ?, ?)",(save_image_to_database(user_icon_filename), save_image_to_database(folder_pic_filename),save_image_to_database(book_pic_filename))
#     db.session.execute(sql)
#     db.session.commit()

def upload(filename, username):
    user_name = session.get("username")
    print(filename)
    print(save_image_to_database(filename))
    sql = text("INSERT INTO images (user_icon, username) VALUES (:user_icon_data, :username)")
    print(sql, {"user_icon": save_image_to_database(filename)})
    db.session.execute(sql, {"user_icon_data": save_image_to_database(filename)}, {"username": user_name})
    db.session.commit()

def user_icon(username):
    user_name = session.get("username")
    sql = text("SELECT user_icon FROM images WHERE username = ?")
    db.session.execute(sql, {"username": user_name})
    db.session.commit()


def update_user_info(user_id, new_username, new_password):
    try:
        sql = "UPDATE users SET name = %s, password = %s WHERE id = %s"
        db.session.execute(sql, (new_username, new_password, user_id))
        db.session.commit()
    except Exception as e:
        # Handle errors, log or raise an exception
        print("Error updating user info:", e)
        db.session.rollback()
    # finally:
    #     cursor.close()
    #     conn.close()
