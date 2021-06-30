import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    birthdays = db.execute("SELECT * FROM birthdays")

    if request.method == "POST":
        if 'name' in request.form:
            name = request.form.get("name")
            month = request.form.get("month")
            day = request.form.get("day")

            matches = db.execute("SELECT * FROM birthdays WHERE name = ?", name.title())

            # If the person entered is already in the database, return an error
            if len(matches) > 0:
                return render_template("error.html", message="You are trying to add a person that is already present on the list.")
            
            # .title() auto capitalizes the first letter of each string present in the name entered
            db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)",
                    name.title(), month, day)

            return redirect("/")

        # Removes a birthday
        elif 'nameDel' in request.form:
            name = request.form.get("nameDel")

            matches = db.execute("SELECT * FROM birthdays WHERE name = ?", name.title())

            if len(matches) == 0:
                return render_template("error.html", message="The person entered isn't present on the list.")
 
            db.execute("DELETE FROM birthdays WHERE name = ?", name.title())

            return redirect("/")

    else:
        return render_template("index.html", birthdays=birthdays)
