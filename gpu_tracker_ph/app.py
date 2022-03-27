from flask import Flask

app = Flask(__name__)


@app.route("/api")
def hello():
    return "<p>Hello, world!</p>"
