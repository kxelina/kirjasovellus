from app import app
from flask import redirect, request, render_template, session
from werkzeug.utils import secure_filename
import os
import users


@app.route("/folders")
def folders():
    user_icon = users.user_icon()
    return render_template("folders.html", user_icon=user_icon)

@app.route("/book")
def book():
    return render_template("book.html")

@app.route("/", methods=["post", "get"])
def create_new_user():
    if request.method == "POST":
        
        username = request.form["username"]
        if len(username) < 1 or len(username) > 10:
            return render_template("error.html", message="your username should contain 1-10 characters")

        password = request.form["password"]
        if password == "":
            return render_template("error.html", message="you should have a password")


        if not users.create_new_user(username, password):
            return render_template("error.html", message="your user hasn't been created")
        return redirect("/")
    return render_template("welcome.html")
    
@app.route("/app", methods=["post", "get"])
def login():
    print("login")
    if request.method == "POST":    
        
        username = request.form["username"]
        password = request.form["password"]
        

        if not username or not password:
            return render_template("error.html", message="fill in both fields")

        
        if not users.login(username, password):
            return render_template("error.html", message="wrong username or password")
    user_icon = users.user_icon()
    print(user_icon)
    return render_template("app.html", user_icon=user_icon)



@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/upload", methods=["post", "get"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    
    if request.method == "POST":
        try :
            print("hello")
            print(request.files)
            user_icon = request.files['user_icon']
            print("12")
            # folder_pic = request.files['folder_pic']
            # print("123")
            # book_pic = request.files['book_pic']

            print(user_icon.filename)
            user_icon_filename = secure_filename(user_icon.filename)
            # folder_pic_filename = secure_filename(folder_pic.filename)
            # book_pic_filename = secure_filename(book_pic.filename)
            print("hah")
            filename = os.path.join(app.config["UPLOAD_FOLDER"], user_icon_filename)
            user_icon.save(filename)
            # folder_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], folder_pic_filename))
            # book_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], book_pic_filename))
            print(filename)
            users.upload(filename)
            print("hello3")
            return  redirect("/app")
        except Exception as e:
       # By this way we can know about the type of error occurring
            print("The error is: ",e)
            return "error"
        

    return redirect("/")


@app.route("/settings", methods=["post", "get"])
def settings():
    if request.method == "POST":
        new_username = request.form["new_username"]
        new_password = request.form["new_password"]
            
        user_id = users.user_id()

        users.update_user_info(user_id, new_username, new_password)
        return redirect("/app")  

    
    return render_template("settings.html")

@app.route("/folders", methods=["post"])
def add_folder():
    if request.method == "POST":
        folder_name = request.form['folder_name']
        
        return redirect("/app")

    
    return redirect("/app")




