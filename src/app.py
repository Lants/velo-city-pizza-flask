# localhost:5000 in  browser to view the webpage. Refresh to see changes.

# Note: DO NOT SET DEBUG MODE IF DEPLOYING PUBLICLY!!! ---------------------------------------------------
#   Debug mode allows for arbitrary code executions from the deployed site.

from flask import Flask, render_template, url_for, request, session
from flask_socketio import SocketIO
import configparser

app = Flask(__name__)
app.config.from_pyfile('config.py')
socketio = SocketIO(app)

# ---- Per-Page Dictionaries for variable access ----
ORDER_ONLINE = {}

# Index (Home) page route
@app.route("/")
@app.route("/home")
@app.route("/index.html")
def index():
    return render_template("index.html")

# Order Ahead (pickup) page route
@app.route("/order_ahead")
def order_ahead():
    return render_template("order_ahead.html", order_online = ORDER_ONLINE)

# ---------- Helper Functions --------------

# Parse pizzas file
def parse_pizzas():
    pizzas = configparser.ConfigParser()
    pizzas.read("square_tools/pizzas.ini")
    return [(list(tuple)[0].title().strip("\""), tuple[1].strip("\"")) for tuple in pizzas.items("PIZZAS")]

# Parse starters file
def parse_starters():
    starters = configparser.ConfigParser()
    starters.read("square_tools/starters.ini")
    return [(list(tuple)[0].title().strip("\""), tuple[1].strip("\"")) for tuple in starters.items("STARTERS")]

# ######################## SOCKET IO #########################

#----------Order Ahead-----------

@socketio.on("order-ahead-ready")
def handle_order_ahead_ready():
    print("Order Ahead: user has connected.")

if __name__ == '__main__':
    ORDER_ONLINE['starters'] = parse_starters()
    ORDER_ONLINE['pizzas'] = parse_pizzas()
    socketio.run(app, debug=True) ### CHANGE ME TO FALSE FOR PUBLIC DEPLOYMENT
    