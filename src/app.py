# localhost:5000 in  browser to view the webpage. Refresh to see changes.

# Note: DO NOT SET DEBUG MODE IF DEPLOYING PUBLICLY!!! ---------------------------------------------------
#   Debug mode allows for arbitrary code executions from the deployed site.

from flask import Flask, render_template, url_for, request

app = Flask(__name__)

# Index (Home) page route
@app.route("/")
@app.route("/home")
@app.route("/index.html")
def index():
    return render_template("index.html")





if __name__ == '__main__':
    app.run(debug=True) ### CHANGE ME TO FALSE FOR PUBLIC DEPLOYMENT