from app import app
from flask import redirect, request, render_template
from werkzeug.utils import secure_filename
import os
import users

def error(e, request, route, link):
    error = f"The error is {route}({request.method}): {e}"
    print(error)
    error2 = f"({request.method}) in {route}: {type(e).__name__}"
    return render_template("error.html", message=error2, link=link)

@app.route("/")
def welcome():
    try:
        return render_template("welcome.html")
    except Exception as e:
        return error(e, request, "/", "")
    
@app.route("/create_user", methods=["post"])
def create_new_user():
    try:
        if request.method == "POST":
            username = request.form["username"]
            if len(username) < 1 or len(username) > 10:
                return render_template("error.html", message="your username should contain 1-10 characters")

            password1 = request.form["password1"]
            password2 = request.form["password2"]
            if password1 == "" or password2 == "":
                return render_template("error.html", message="you should have a password")
            
            if password1 != password2:
                return render_template("error.html", message="your passwords are different")

            if not users.create_new_user(username, password1):
                return render_template("error.html", message="your user hasn't been created, username is in use")
            return redirect("/app")
        
    except Exception as e:
        return error(e, request, "/create_user", "")
    
@app.route("/app", methods=["post", "get"])
def login():
    try:
        if request.method == "POST":    
            username = request.form["username"]
            password = request.form["password"]
            
            if not username or not password:
                return render_template("error.html", message="fill in both fields")

            if not users.login(username, password):
                return render_template("error.html", message="wrong username or password")
            return redirect("/app")
        
        if request.method == "GET":
            users.check_csrf_token()
            books = users.get_books()
            user_icon = users.get_user_icon()
            book_pic = app.config["BOOK_FOLDER"]
            return render_template("app.html", books=books, user_icon=user_icon, book_pic= book_pic)
    
    except Exception as e:
        return error(e, request, "/app", "")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/folders", methods=["post", "get"])
def folders():
    try:
        if request.method == "POST":
            users.check_csrf()
            folder_name = request.form["folder_name"]
            users.add_folders(folder_name)
            return redirect("/folders")
        
        if request.method == "GET":
            users.check_csrf_token()
            user_icon = users.get_user_icon()
            folder = users.get_folders()
            return render_template("folders.html", user_icon=user_icon, folders=folder)  
        
    except Exception as e:
        return error(e, request, "/folders", "app")

@app.route("/book", methods=["post", "get"])
def book():
    try:
        if request.method == "POST":
            users.check_csrf()
            title = request.form["title"]
            author = request.form["author"]
            year = request.form["publication_year"] 
            description = request.form["description_text"]
            genre = request.form["genre"]
            users.add_book(title, author, year, description, genre)
        
            return redirect("/app")

        if request.method == "GET":
            users.check_csrf_token()
            books = users.get_books()
            if books == []:
                return redirect("/app")
            return render_template("book.html", books=books)

    except Exception as e:
        return error(e, request, "/book", "app")

@app.route("/upload", methods=["post", "get"])
def upload():
    try :
        if request.method == "GET":
            users.check_csrf_token()
            return render_template("upload.html")
        
        if request.method == "POST":
            users.check_csrf()
            user_icon = request.files["user_icon"]
            user_icon_filename = secure_filename(user_icon.filename)
            filename = os.path.join(app.config["UPLOAD_FOLDER"], user_icon_filename)
            user_icon.save(filename)
            if users.upload_user_icon(filename):
                return redirect("/app")
            return render_template("error.html", message="Invalid image file, try another image file", link="app")
            
    except Exception as e:
        return error(e, request, "/upload", "app")

@app.route("/settings", methods=["post", "get"])
def settings():
    try: 
        if request.method == "POST":
            users.check_csrf()
            new_password1 = request.form["new_password1"]
            new_password2 = request.form["new_password2"]
            if new_password1 == "" or new_password2 == "":
                return render_template("error.html", message="you should have a password", link="app")
            
            if new_password1 != new_password2:
                return render_template("error.html", message="your passwords are different", link="app")
            
            user_id = users.get_user_id()
            users.update_user_info(user_id, new_password1)
            return redirect("/app")  

        if request.method == "GET":
            users.check_csrf_token()
            return render_template("settings.html")
    
    except Exception as e:
        return error(e, request, "/settings", "app")

@app.route('/book/<book_id>',  methods=["post", "get"])
def book_details(book_id):
    try:
        if request.method == "POST":
            users.check_csrf()
            folders = request.form["folder_id"]
            users.add_book_to_folder(book_id, folders) 
            return redirect("/folders")
        
        if request.method == "GET":
            users.check_csrf_token()
            folders = users.get_folders()
            book = users.get_book(book_id)
            reviews = users.get_reviews(book_id)
            book_pic = f"../{users.get_book_pic(book_id)}"
            return render_template("book.html", book=book, folders=folders, reviews=reviews, book_pic=book_pic)

    except Exception as e:
        return error(e, request, "/book/book_id", "app")
    
@app.route('/review/book/<book_id>',  methods=["post"])
def reviews(book_id):
    try:
        if request.method == "POST":
            users.check_csrf()
            review = request.form["review_text"]
            rating = request.form["rating"]
            users.add_review(book_id, review, rating)
            return redirect(f"/book/{book_id}")

    except Exception as e:
        return error(e, request, "/review", "app")
    
@app.route('/folder/<folder_id>',  methods=["get","post"])
def folder_books(folder_id):
    try:
        if request.method == "GET":
            users.check_csrf_token()
            books_in_folder = users.get_books_in_folder(folder_id)
            book_pic = f"../{app.config['BOOK_FOLDER']}"
            folders = users.get_foldername_by_id(folder_id)  
            return render_template("booklist.html", books=books_in_folder, folder_name=folders, book_pic=book_pic)
        
        if request.method == "POST":
            users.check_csrf()
            book_id = request.form["book_id"]
            users.remove_book_from_folder(folder_id, book_id)
            return redirect(f"/folder/{folder_id}")

    except Exception as e:
        return error(e, request, "/folder", "app")
    
@app.route('/upload/<book_id>',  methods=["post"])
def upload_book_pic(book_id):
    try:
        if request.method == "POST":
            users.check_csrf()
            book_pic = request.files["book_cover"]
            book_pic_filename = secure_filename(book_pic.filename)
            filename = os.path.join(app.config["UPLOAD_FOLDER"], book_pic_filename)
            book_pic.save(filename)
            if users.upload_book_pic(filename, book_id):
                return redirect(f"/book/{book_id}")
            return render_template("error.html", message="Invalid image file, try another image file", link="app")

    except Exception as e:
        return error(e, request, "/upload/book_id", "app")






