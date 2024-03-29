import os
import io
import psycopg2
from PIL import Image
from flask import session
from sqlalchemy.sql import text
from app import app
from db import db


def read_image_from_path(image_path):
    with open(image_path, 'rb') as file:
        image_data = file.read()
    Image.open(io.BytesIO(image_data))
    return psycopg2.Binary(image_data)


def upload_book_pic(filename, book_id):
    file_name, file_extension = os.path.splitext(filename)
    sql = text(
        '''INSERT INTO book_images (picture_data, book_id, file_extension)
        VALUES (:picture_data, :book_id, :file_extension) ON CONFLICT (book_id)
        DO UPDATE SET file_extension = :file_extension, picture_data = :picture_data''')
    try:
        image = read_image_from_path(filename)
    except Exception as error:
        print(error)
        return False
    db.session.execute(sql, {"picture_data": image,
                       "book_id": book_id, "file_extension": file_extension})
    db.session.commit()
    return True


def get_book_pic(book_id):
    sql = text(
        "SELECT picture_data, file_extension FROM book_images WHERE book_id = :book_id")
    result = db.session.execute(sql, {"book_id": book_id})
    file_data = result.fetchone()

    if file_data is None:
        filename = "/static/images/default-book-cover.png"
    else:
        filename = os.path.join(
            app.config["BOOK_FOLDER"], book_id + file_data[1])
        image_data = io.BytesIO(file_data[0])
        image = Image.open(image_data)
        image.save(filename)
    return filename


def add_folders(folder_name, user_name=None):
    if user_name is None:
        user_name = session.get("username")
    sql = text(
        "INSERT INTO folders (folder_name, username) VALUES (:folder_name, :username)")
    db.session.execute(
        sql, {"folder_name": folder_name, "username": user_name})
    db.session.commit()


def get_folders():
    user_name = session.get("username")
    sql = text(
        "SELECT folder_id, folder_name FROM folders WHERE username = :username")
    result = db.session.execute(sql, {"username": user_name})
    folders = result.fetchall()
    return folders


def add_book(title, author, publication_year, description_text, genre):
    sql = text(
        '''INSERT INTO books (title, author, publication_year, description_text, genre)
        VALUES (:title, :author, :publication_year, :description_text, :genre)''')
    db.session.execute(sql, {
        "title": title,
        "author": author,
        "publication_year": publication_year,
        "description_text": description_text,
        "genre": genre
    })
    db.session.commit()


def get_books():
    sql = text(
        '''SELECT A.book_id, title, author, publication_year,
        description_text, genre, file_extension
        FROM books AS A LEFT JOIN book_images AS B ON A.book_id = B.book_id''')
    result = db.session.execute(sql)
    book = result.fetchall()
    return book


def get_book(book_id):
    sql = text(
        '''SELECT book_id, title, author, publication_year, description_text, genre
        FROM books WHERE book_id = :book_id''')
    result = db.session.execute(sql, {"book_id": book_id})
    book = result.fetchone()
    return book


def add_book_to_folder(book_id, folder_id):
    user_name = session.get("username")
    sql = text(
        '''INSERT INTO books_in_folder (book_id, folder_id, username)
        VALUES (:book_id, :folder_id, :username)''')
    db.session.execute(
        sql, {"book_id": book_id, "folder_id": folder_id, "username": user_name})
    db.session.commit()


def get_books_in_folder(folder_id):
    user_name = session.get("username")
    sql = text(
        '''SELECT B.title, B.author, B.book_id, I.file_extension, folder_id FROM books AS B
        LEFT JOIN books_in_folder AS F ON B.book_id = F.book_id
        LEFT JOIN book_images AS I ON B.book_id = I.book_id
        WHERE username = :username AND folder_id = :folder_id''')
    result = db.session.execute(
        sql, {"username": user_name, "folder_id": folder_id})
    books = result.fetchall()
    return books


def remove_book_from_folder(folder_id, book_id):
    user_name = session.get("username")
    sql = text(
        '''DELETE FROM books_in_folder
        WHERE folder_id = :folder_id AND username = :username AND book_id = :book_id''')
    db.session.execute(sql, {"folder_id": folder_id,
                       "book_id": book_id, "username": user_name})
    db.session.commit()


def get_foldername_by_id(folder_id):
    sql = text("SELECT folder_name FROM folders WHERE folder_id = :folder_id")
    result = db.session.execute(sql, {"folder_id": folder_id})
    foldername = result.fetchone()
    return foldername[0]


def add_review(book_id, review_text, rating):
    user_name = session.get("username")
    sql = text(
        '''INSERT INTO review (book_id, review_text, username, rating)
        VALUES (:book_id, :review_text, :username, :rating)''')
    db.session.execute(sql, {"book_id": book_id, "username": user_name,
                       "review_text": review_text, "rating": rating})
    db.session.commit()


def get_reviews(book_id):
    sql = text(
        "SELECT review_text, rating, username FROM review WHERE book_id = :book_id")
    result = db.session.execute(sql, {"book_id": book_id})
    reviews = result.fetchall()
    return reviews
