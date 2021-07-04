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

SPECIAL = ['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', '-', '.', ',', '/', ':', ';',
           '<', '>', '=', '?', '@', '[', ']', '^', '_', '`', '{', '}', '|', '~', "'"]


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Gets all the relevant stock information
    symbolShares = db.execute("SELECT symbol, current_shares FROM portfolio where user_id = ?", session["user_id"])

    # creates 2 lists with symbols / shares from all the stocks the user has
    symbols = []
    shares = []
    for dictionary in symbolShares:
        symbols.append(dictionary["symbol"])
        shares.append(dictionary["current_shares"])

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

    # turns the total and prices into a dict associated with the stock symbol
    totalDict = dict(zip(symbols, total))
    priceDict = dict(zip(symbols, prices))

    # Delete from the portfolio if the user has 0 shares
    for share in shares:
        if share == 0:
            db.execute("DELETE FROM portfolio WHERE current_shares = 0")

    # updates the total and prices with the latest information on the DB
    for key in totalDict:
        db.execute("UPDATE portfolio SET current_total = ? WHERE symbol = ? AND user_id = ?",
                   totalDict[key], key, session["user_id"])
    for key in priceDict:
        db.execute("UPDATE portfolio SET current_price = ? WHERE symbol = ? AND user_id = ?",
                   priceDict[key], key, session["user_id"])

    # selects the cash the user current has
    cash = db.execute("SELECT cash from users WHERE id = ?", session["user_id"])
    for dictionary in cash:
        cash = dictionary["cash"]
    
    # Calculates the total
    TOTAL = cash

    for item in total:
        TOTAL += item

    # If the user doesn't own any stocks yet, display an empty page
    portfolio = db.execute("SELECT * FROM portfolio WHERE user_id = ?", session["user_id"])
    if len(portfolio) == 0:
        return render_template("empty.html", sender="portfolio", cash=cash)

    return render_template("index.html", portfolio=portfolio, cash=cash, total=TOTAL)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        # Gets the inputted symbol and number of shares
        symbol = request.form.get("symbol")
        shares_transacted = request.form.get("shares")

        # Checks if the input fields are blank
        if symbol == '':
            return apology("must provide symbol")
        elif shares_transacted == '':
            return apology("must provide number of shares")

        if not shares_transacted.isdigit():
            return apology("must provide valid number of shares")

        # Converts the number of shares to an integer
        shares_transacted = int(shares_transacted)

        # Checks if the number of shares the user is trying to buy is valid
        if shares_transacted < 1:
            return apology("must provide valid number of shares")

        # Gets the information about it
        stock_info = lookup(symbol)

        # If the symbol entered is invalid
        if stock_info == None:
            return apology("invalid symbol")

        # Gets the name and price of the stock
        name = stock_info["name"]
        price = stock_info["price"]

        purchase_total = price * shares_transacted

        # Gets the cash the current user has
        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        for dictionary in current_cash:
            current_cash = dictionary["cash"]

        # If the user can't afford the purchase
        if current_cash < purchase_total:
            return apology("can't afford")

        # Purchase process
        current_cash = current_cash - purchase_total

        # Updates the DB
        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash, session["user_id"])

        # Gets the date and time
        date = datetime.today().strftime('%Y/%m/%d')
        time = datetime.today().strftime('%H:%M:%S')

        # register the purchase
        db.execute("INSERT INTO history (transaction_type, user_id, symbol, name, transacted_shares, transacted_price, transacted_total, date, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   "PURCHASE", session["user_id"], symbol, name, shares_transacted, price, purchase_total, date, time)

        # Checks if it's the first purchase of a stock (to INSERT it) otherwise, UPDATE it
        current_shares = db.execute("SELECT current_shares FROM portfolio WHERE user_id = ? AND symbol = ?",
                                    session["user_id"], symbol)
        if len(current_shares) == 0:
            # Log the purchase
            db.execute("INSERT INTO portfolio (user_id, symbol, name, current_shares, current_price, current_total) VALUES (?, ?, ?, ?, ?, ?)",
                       session["user_id"], symbol, name, shares_transacted, price, purchase_total)
        else:
            for dictionary in current_shares:
                current_shares = dictionary["current_shares"]

            # Update the index page with the latest information
            total_shares = current_shares + shares_transacted
            updated_total = price * total_shares

            db.execute("UPDATE portfolio SET current_shares = ?, current_price = ?, current_total = ? WHERE user_id = ? AND symbol = ?",
                       total_shares, price, updated_total, session["user_id"], symbol)

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM history where user_id = ?", session["user_id"])

    # Renders another page if the history is empty
    if len(history) == 0:
        return render_template("empty.html", sender="history")

    # reverses the list for the latest information appear on the top
    reversedHist = []

    for dictionary in reversed(history):
        reversedHist.append(dictionary)

    return render_template("history.html", history=reversedHist)


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
            return apology("must provide username", 400)

        elif not password:
            return apology("must provide password", 400)

        elif not confirmation:
            return apology("must confirm password", 400)

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
            return apology("password should contain at least one number")

        elif not any(char.isupper() for char in password):
            return apology("password should contain at least one uppercase letter")

        elif not any(char.islower() for char in password):
            return apology("password should contain at least one lowercase letter")

        elif not any(char in SPECIAL for char in password):
            return apology("password should have at least one special character")

        # Inserts the new user into the DB
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    # Allows the user to add money
    # Gets the user's current cash
    current_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    for dictionary in current_cash:
        current_cash = dictionary["cash"]

    if request.method == "POST":
        quantity = request.form.get("quantity")

        if quantity == '':
            return apology("must provide the quantity")

        if not quantity.isdigit():
            return apology("must provide a valid quantity")

        # Converts the quantity to an integer
        quantity = int(quantity)

        # allows only adding 1000 dollars at a time
        if quantity < 0 or quantity > 1000:
            return apology("invalid quantity (max: $1000.00)")

        # Gets the date and time
        date = datetime.today().strftime('%Y/%m/%d')
        time = datetime.today().strftime('%H:%M:%S')

        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash + quantity, session["user_id"])

        # logs
        db.execute("INSERT INTO history (transaction_type, user_id, symbol, name, transacted_shares, transacted_price, transacted_total, date, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   "CHARGE", session["user_id"], "-", "-", 0, quantity, quantity, date, time)
        return redirect("/")

    else:
        return render_template("add.html", cash=current_cash)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Gets all the symbols for the stocks the current user has, puts them on a list and displays
    # them on the selector when loading the page
    symbolsDict = db.execute("SELECT symbol FROM portfolio WHERE user_id = ?", session["user_id"])
    symbols = []
    for dictionary in symbolsDict:
        symbols.append(dictionary["symbol"])

    if request.method == "POST":

        # Gets the inputted symbol
        symbol = request.form.get("symbol")
        shares_transacted = request.form.get("shares")

        # ERROR CHECKING
        if symbol == "":
            return apology("missing symbol")
        if symbol not in symbols:
            return apology("invalid symbol")
        elif shares_transacted == '':
            return apology("must provide number of shares")

        if not shares_transacted.isdigit():
            return apology("must provide valid number of shares")

        # Converts the number of shares to an integer
        shares_transacted = int(shares_transacted)

        # Checks if the number of shares the user is trying to sell is valid
        if shares_transacted < 1:
            return apology("must provide valid number of shares")

        current_shares = db.execute("SELECT current_shares FROM portfolio WHERE user_id = ? AND symbol = ?", 
                                    session["user_id"], symbol)
        print(current_shares)
        for dictionary in current_shares:
            current_shares = dictionary["current_shares"]

        # If 0 elements is found, convert the empty list returned into the int 0
        if current_shares == []:
            current_shares = 0

        # If the num of shares the user has is less then the num of shares they wanna sell
        if current_shares < shares_transacted:
            return apology("too many shares")

        # Gets information about stock
        stock_info = lookup(symbol)
        # Gets the price / name of the stock
        price = stock_info["price"]
        name = stock_info["name"]

        # calculates the transaction total
        transaction_total = price * shares_transacted

        # calculates the symbol's total
        total = price * (current_shares - shares_transacted)

        db.execute("UPDATE portfolio SET current_shares = ?, current_price = ?, current_total = ? WHERE user_id = ? AND symbol = ?", 
                   current_shares - shares_transacted, price, total, session["user_id"], symbol)

        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        for dictionary in current_cash:
            current_cash = dictionary["cash"]

        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash + transaction_total, session["user_id"])

        # Gets the date and time
        date = datetime.today().strftime('%Y/%m/%d')
        time = datetime.today().strftime('%H:%M:%S')

        db.execute("INSERT INTO history (transaction_type, user_id, symbol, name, transacted_shares, transacted_price, transacted_total, date, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   "SELL", session["user_id"], symbol, name, shares_transacted, price, transaction_total, date, time)

        return redirect("/")

    else:
        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
