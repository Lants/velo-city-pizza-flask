# localhost:5000 in  browser to view the webpage. Refresh to see changes.

# Note: DO NOT SET DEBUG MODE IF DEPLOYING PUBLICLY!!! ---------------------------------------------------
#   Debug mode allows for arbitrary code executions from the deployed site.

from flask import Flask, render_template, url_for, request, session
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_pyfile('config.py')
socketio = SocketIO(app)

# Index (Home) page route
@app.route("/")
@app.route("/home")
@app.route("/index.html")
def index():
    return render_template("index.html")

# Order Ahead (pickup) page route
@app.route("/order_ahead")
def order_ahead():
    return render_template("order_ahead.html")


# ######################## SOCKET IO #########################

#----------Order Ahead-----------

@socketio.on("order-ahead-ready")
def handle_order_ahead_ready():
    print("Order Ahead: user has connected.")

if __name__ == '__main__':
    socketio.run(app, debug=True) ### CHANGE ME TO FALSE FOR PUBLIC DEPLOYMENT