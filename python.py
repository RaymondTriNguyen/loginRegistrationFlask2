import sqlite3
from flask import Flask, render_template, redirect, request, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.secret_key="abc123"

def create_database():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        "Create table if not exists user (id integer primary key autoincrement, username text not null unique, email text not null unique, password text not null)")
    conn.commit()
    conn.close()
create_database()

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory=sqlite3.Row
    return conn



'''
def init_db():
    conn=get_db_connection()
    conn.execute("Create table if not exists user (id integer primary key autoincrement, username text not null unique, password text not null)")
    conn.commit()
    conn.close()
    
    '''
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="POST":
        username=request.form["username"]
        email=request.form["email"]
        password=request.form["password"]
        hashed_password=generate_password_hash(password)
        conn=get_db_connection()
        cur=conn.cursor()
        cur.execute("Insert into user (username, email, password) values (?, ?, ?)", (username, email, hashed_password))
        conn.commit()
        conn.close()
        flash("Registration successful.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/")
def default():
    return render_template("launch.html")


@app.route("/login", methods=["GET", "POST"])
def login():
     if request.method=="POST":
         email=request.form["email"]
         password=request.form["password"]
         hashed_password = generate_password_hash(password)
         conn=get_db_connection()
         cur=conn.cursor()
         cur.execute("Select * from user where email=?", (email,))
         user=cur.fetchone()
         conn.close()
         if user and check_password_hash(user["password"], password):

             flash("Login Successful", 'success')
             return redirect(url_for("welcome", username=user["username"]))
         else:
             flash("Login failed. Please check your username and password.", 'danger')
     return render_template("login.html")
@app.route("/welcome")


def welcome():
    username=request.args.get("username")
    if not username:
        flash("Login to access the website.","warning")
        return redirect(url_for("login"))
    return render_template("welcome.html",username=username)

if __name__=="__main__":
    app.run(debug=True)