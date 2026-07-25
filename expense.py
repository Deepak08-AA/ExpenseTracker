from flask import render_template, redirect, request, session,url_for

from app import app
from database import get_records, add_record, update_record, delete_record, check_record
from analytics import (
    total_expense,
    max_expense,
    min_expense,
    expense_by_category

)

@app.route("/home")
def home():

    if "user_id" not in session:
        return redirect("/")
    
    user_id = session["user_id"]
    expenses = get_records(user_id)

    total = total_expense(user_id)
    maximum = max_expense(user_id)
    minimum = min_expense(user_id)
    # average = average_expense(user_id)
    category_data = expense_by_category(user_id)

    return render_template(
        "home.html",
        expenses=expenses,
        total=total,
        maximum=maximum,
        minimum=minimum,
        category_data=category_data,
        Name=session["username"]
    )

@app.route("/add", methods=["GET", "POST"])
def add():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        user_id = session["user_id"]
        amount = request.form["amount"]
        category = request.form["category"]
        payment_method = request.form["payment_method"]
        date = request.form["date"]

        add_record(user_id,amount,category,payment_method,date)

        return redirect(url_for("home"))

    return render_template("add.html")


@app.route("/delete/<int:id>")
def delete(id):

    if "user_id" not in session:
        return redirect("/")

    delete_record(session["user_id"], id)

    return redirect(url_for("home"))


@app.route("/update/<int:id>", methods=["GET", "POST"])
def edit(id):

    if "user_id" not in session:
        return redirect('/')

    if request.method == "POST":

        amount = request.form["amount"]
        category = request.form["category"]
        payment_method = request.form["payment_method"]
        date = request.form["date"]

        update_record(session["user_id"], id, amount, category, payment_method, date)

        return redirect(url_for("home"))

    expense = check_record(session["user_id"], id)

    return render_template("edit.html",expense=expense)
