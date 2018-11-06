from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)
@app.route("/")
def index():
    return redirect("/users")

@app.route("/users")
def users():
    mysql = connectToMySQL("users")
    all_users = mysql.query_db("SELECT * FROM users;")
    return render_template("users.html", users = all_users)

@app.route("/users/new")
def new():
    return render_template("new.html")

@app.route("/users/create", methods=["POST"])
def create():
    mysql = connectToMySQL("users")
    query = "INSERT INTO users(full_name, email) VALUES(%(n)s, %(e)s);"
    data = {
        'n': request.form["first_name"] + " " + request.form["last_name"],
        'e': request.form["email"],
    }
    new_user_id = mysql.query_db(query, data)
    return redirect(f"/users/{new_user_id}")

@app.route("/users/<num>")
def profile(num):
    num = int(num)
    mysql = connectToMySQL("users") #try just one user passed
    my_user = mysql.query_db(f"SELECT * FROM users WHERE id = '{num}';")
    return render_template("user_profile.html", user = my_user[0], id = num)

@app.route("/users/<num>/edit")
def edit(num):
    num = int(num)
    mysql = connectToMySQL("users")
    return render_template("edit.html", id = num)

@app.route("/users/<num>/update", methods = ["POST"])
def update(num):
    mysql = connectToMySQL("users") #try just one user passed
    query = "UPDATE users SET full_name = %(n)s, email = %(e)s WHERE id = %(i)s;"
    data = {
        'n': request.form["first_name"] + " " + request.form["last_name"],
        'e': request.form["email"],
        'i': int(num),
    }
    num = int(num)
    yoink = mysql.query_db(query, data)
    return redirect(f"/users/{num}")

@app.route("/users/<num>/destroy")
def destroy(num):
    num = int(num)
    mysql = connectToMySQL("users")
    yeet = mysql.query_db(f"DELETE FROM users WHERE id = '{num}';")
    return redirect("/users")

if __name__ == "__main__":
    app.run(debug=True)