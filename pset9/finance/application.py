import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

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


@app.route("/")
@login_required
def index():
    total = db.execute("SELECT symbol, SUM(shares) as total FROM history WHERE user_id = ? GROUP BY symbol HAVING total > 0", session["user_id"])

    rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = rows[0]["cash"]

    stocks = []

    fulltotal = 0

    for row in total:
        stock = lookup(row["symbol"])
        stocks.append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "shares": row["total"],
            "price": stock["price"],
            "total": usd(stock["price"] * row["total"])
        })
        fulltotal += stock["price"] * row["total"]

    fulltotal += cash
    return render_template("index.html", stocks = stocks, cash = usd(cash), fulltotal = usd(fulltotal))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        elif not request.form.get("shares"):
            return apology("must provide number of shares", 400)
        elif not request.form.get("shares").isdigit():
            return apology("number of shares must be whole number")

        symbol = request.form.get("symbol").upper()
        stock = lookup(symbol)

        if stock is None:
            return apology("Invalid Ticker Symbol", 400)

        shares = int(request.form.get("shares"))
        price = stock['price']


        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        currentcash = cash[0]["cash"]
        if (shares * price) > currentcash:
            return apology("Not enough cash")

        db.execute("UPDATE users SET cash = ? WHERE id = ?", currentcash - (shares * price), session["user_id"])
        db.execute("INSERT INTO history (user_id, symbol, shares, price) VALUES(?,?,?,?)", session["user_id"], symbol, shares, price)

        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    rows = db.execute("SELECT * FROM history WHERE user_id = ?", session["user_id"])
    
    for row in rows:
        row["price"] = usd(row["price"])
    
    return render_template("history.html", rows = rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide a ticker symbol", 400)
        symbol = request.form.get("symbol").upper()
        stock = lookup(symbol)
        if stock is None:
            return apology("Invalid Ticker Symbol", 400)
        return render_template("stockquote.html", stock = {'name': stock['name'], 'price': usd(stock['price']), 'symbol': stock['symbol']})
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        elif (request.form.get("password")) != (request.form.get("confirmation")):
            return apology("passwords don't match", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 0:
            return apology("username taken", 400)

        idkey = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        if idkey is None:
            return apology("Error with registration", 400)

        session["user_id"] = idkey

        flash("Registered!")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        elif not request.form.get("shares"):
            return apology("must provide number of shares", 400)
        elif not request.form.get("shares").isdigit():
            return apology("number of shares must be whole number")


        symbol = request.form.get("symbol").upper()
        stock = lookup(symbol)

        if stock is None:
            return apology("Invalid Ticker Symbol", 400)

        rows =  db.execute("SELECT * FROM history WHERE user_id = :user_id AND symbol = :symbol", user_id= session["user_id"], symbol=symbol)
        
        total = 0
        
        for row in rows:
            total += row["shares"]
        
        shares = int(request.form.get("shares"))
        price = stock['price']
        
        if shares > total:
            return apology("Not enough shares owned")

        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        currentcash = cash[0]["cash"]


        db.execute("UPDATE users SET cash = ? WHERE id = ?", currentcash + (shares * price), session["user_id"])
        db.execute("INSERT INTO history (user_id, symbol, shares, price) VALUES(?,?,?,?)", session["user_id"], symbol, -shares, price)

        flash("Sold!")
        return redirect("/")

    else:
        rows = db.execute("SELECT symbol FROM history WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
        symbols = []
        for row in rows:
            symbols.append(row["symbol"])
        return render_template("sell.html", symbols = symbols)
        

@app.route("/changepass", methods=["GET", "POST"])
@login_required
def changepass():
    if request.method == "POST":

        if not request.form.get("newpass"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmpass"):
            return apology("must confirm password", 400)

        elif (request.form.get("newpass")) != (request.form.get("confirmpass")):
            return apology("passwords don't match", 400)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(request.form.get("newpass")), session["user_id"])
        
        flash("Reset Password!")
        return redirect("/")
    else:
        return render_template("password.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
