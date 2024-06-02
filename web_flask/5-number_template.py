#!/usr/bin/python3
"""
    Module script to start a Flask web application
"""
from flask import Flask, render_template
from markupsafe import escape


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """default route"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """hbnb route"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """c route"""
    modified_text = ""
    for char in escape(text):
        if char == "_":
            modified_text += " "
        else:
            modified_text += char
    return "C " + modified_text


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python', strict_slashes=False)
def py_thon(text="is cool"):
    """python route"""
    modified_text = ""
    for char in escape(text):
        if char == "_":
            modified_text += " "
        else:
            modified_text += char
    return "Python " + modified_text


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """number route"""
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """number template route"""
    return render_template("5-number.html", n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
