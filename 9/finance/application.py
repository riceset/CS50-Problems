import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

SPECIAL = ['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', '-', '.', ',', '/', ':', ';', '<', '>', '=', '?', '@', '[', ']', '^', '_', '`', '{', '}', '|', '~', "'"]

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    transactions = db.execute("SELECT * FROM transactions")

    # Gets all the relevant stock information
    symbolShares = db.execute("SELECT symbol, shares FROM transactions")

    # creates 3 lists with symbols / shares / price from all the stocks the user has
    symbols = []
    shares = []
    for dictionary in symbolShares:
        symbols.append(dictionary["symbol"])
        shares.append(dictionary["shares"])

    # Gets a list of dictionaries with the newest information for each stock
    incomingInfo = []
    for symbol in symbols:
        incomingInfo.append(lookup(symbol))

    # Gets the price for each stock
    prices = []
    for dictionary in incomingInfo:
        prices.append(dictionary["price"])

    # Multiplies the price of each stock with the quantity the user currently has
    total = []
    for share, price, in zip(shares, prices):
        total.append(share * price)

    totalDict = dict(zip(symbols, total))
    priceDict = dict(zip(symbols, prices))

    for key in totalDict:
        db.execute("UPDATE transactions SET total = ? WHERE symbol = ?", totalDict[key], key)
    for key in priceDict:
        db.execute("UPDATE transactions SET price = ? WHERE symbol = ?", priceDict[key], key)

    cash = db.execute("SELECT cash from users WHERE id = ?", session["user_id"])
    for dictionary in cash:
        cash = dictionary["cash"]

    print(transactions)
    return render_template("index.html", transactions=transactions, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        # Gets the inputted symbol
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Checks if the input fields are blank
        if symbol == '':
            return apology("must provide symbol")
        elif shares == '':
            return apology("must provide number of shares")

        # Converts the number of shares to an integer
        shares = int(shares)

        # Checks if the number of shares the user is trying to buy is valid
        if shares < 1:
            return apology("must provide valid number of shares")

        # Gets the information about it
        stock_info = lookup(symbol)

        # If the symbol entered is invalid
        if stock_info == None:
            return apology("invalid symbol")

        # Gets the name and price of the stock
        name = stock_info["name"]
        price = stock_info["price"]

        # Gets the cash the current user has
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        for dictionary in cash:
            cash = dictionary["cash"]

        total = price * shares

        # If the user can't afford the purchase
        if cash < total:
            return apology("can't afford")

        # Purchase process
        cash = cash - total

        # Updates the DB
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])

        # Gets the date and time
        date = datetime.today().strftime('%Y/%m/%d')
        time = datetime.today().strftime('%H:%M:%S')

        # Inserts all the transaction information into a table
        db.execute("INSERT INTO transactions (symbol, name, price, shares, total, date, time, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", symbol, name, price, shares, total, date, time, session["user_id"])

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # Gets the inputted symbol
        symbol = request.form.get("symbol")

        # Gets the information about it
        stock_info = lookup(symbol)

        # If the symbol entered is invalid
        if stock_info == None:
            return apology("invalid symbol")

        # Gets name and price from the dictionary
        # {'name': 'Apple Inc', 'price': 137.25, 'symbol': 'AAPL'}
        name = stock_info["name"]
        price = stock_info["price"]

        return render_template("quoted.html", name=name, price=price, symbol=symbol)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Getting the username and password entered
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Getting all the matches on the DB for the username entered
        username_matches = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Checks for empty input
        if not username:
            return apology("must provide username", 403)

        elif not password:
            return apology("must provide password", 403)

        elif not confirmation:
            return apology("must confirm password", 403)

        # Checks if the username entered is already registered on the DB
        elif len(username_matches) == 1:
            return apology("the username entered is not available")

        # Checks if the passwords match
        elif (password != confirmation):
            return apology("passwords don't match")

        # Secure Password Check (source: https://www.geeksforgeeks.org/password-validation-in-python/)
        elif len(password) < 6:
            return apology("password must be at least 6 characters")

        elif not any(char.isdigit() for char in password):
            return apology("passwords should contain at least ine number")

        elif not any(char.isupper() for char in password):
            return apology("password should contain at leats one uppercase letter")

        elif not any(char.islower() for char in password):
            return apology("password should contain at leats one lowercase letter")

        elif not any(char in SPECIAL for char in password):
            return apology("passwords should have at least one special character")

        # Inserts the new user into the DB
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
