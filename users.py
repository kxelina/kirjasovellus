import os
import psycopg2
from app import app
from db import db
from flask import abort, request, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from PIL import Image
import io

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
    keys_to_remove = ["user_id", "username", "csrf_token", "user_name"]
    for key in keys_to_remove:
        session.pop(key, None)
    print("keys")
    for key in session:
        print(key)
    print("end")
           

def create_new_user(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
        print("HELLO")
    except Exception as e:
       # By this way we can know about the type of error occurring
        print("The error is: ",e)
        return False

    return True


def update_user_info(user_id, new_username, new_password):
    hash_value = generate_password_hash(new_password)
    try:
        sql = text("UPDATE users SET username = :new_username, password = :new_password WHERE id = :user_id")
        db.session.execute(sql, {"new_username" : new_username, "new_password": hash_value,"user_id": user_id})
        print(user_id)
        db.session.commit()
    except Exception as e:
        # Handle errors, log or raise an exception
        print("Error updating user info:", e)
        db.session.rollback()

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

def upload(filename):
    user_name = session.get("username")
    print(filename)
    print(save_image_to_database(filename))
    file_name, file_extension=os.path.splitext(filename)
    #sql = text("INSERT INTO images (user_icon, username, file_extension) VALUES (:user_icon_data, :username, :file_extension)")
    sql = text("INSERT INTO images (user_icon, username, file_extension) VALUES (:user_icon_data, :username, :file_extension) ON CONFLICT (username) DO UPDATE SET file_extension = :file_extension, user_icon = :user_icon_data")
    print(sql, {"user_icon": save_image_to_database(filename)})
    db.session.execute(sql, {"user_icon_data": save_image_to_database(filename), "username": user_name, "file_extension": file_extension})
    db.session.commit()

def user_icon():
    user_name = session.get("username")
    sql = text("SELECT user_icon, file_extension FROM images WHERE username = :username")
    result = db.session.execute(sql, {"username": user_name})
    file_data = result.fetchone() 
  
    if file_data is None:
        filename = ("static/images/default-profile.jpg")
    else:
        filename = os.path.join(app.config["PROFILE_FOLDER"], user_name + file_data[1])
        print(filename)
        image_data = io.BytesIO(file_data[0])
        
        image = Image.open(image_data)
        image.save(filename)
    return filename
        #image.show()  




    # finally:
    #     cursor.close()
    #     conn.close()

# def show_user_icon():
#     user_name = session.get("username")
#     sql = text("SELECT user_icon FROM images WHERE username = ?")
#     db.session.execute(sql, {"username": user_name})
#     db.session.commit()



