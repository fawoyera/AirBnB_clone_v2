#!/usr/bin/python3
"""
    Module script to start a Flask web application
"""
from flask import Flask, render_template
from markupsafe import escape
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def tear_down(arg):
    """tear down method"""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_():
    """cities route"""
    states = [state for state in storage.all(State).values()]
    return render_template("8-cities_by_states.html", states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
