print("AUTH IMPORTED")

from flask import render_template, redirect, request, session, flash
import bcrypt

from app import app
from database import user_exists, create_user, login_user


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login_validation", methods=["POST"])
def login_validation():

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    user = login_user(username, email)

    if user:
        if bcrypt.checkpw(
            password.encode("utf-8"),
            user["password"].encode("utf-8")
        ):

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["email"] = user["email"]

            return redirect("/home")

    flash("Invalid username, email or password.", "login")
    return redirect("/")


@app.route("/add_user", methods=["POST"])
def add_user():

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if user_exists(username, email):
        flash("Username or Email already exists.", "signup")
        return redirect("/?form=signup")

    create_user(username, email, password)

    flash("Account created successfully. Please login.", "login")
    return redirect("/")


@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "login")

    return redirect("/")

print("END OF AUTH")