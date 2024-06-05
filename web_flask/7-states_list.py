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


@app.route('/states_list', strict_slashes=False)
def states_():
    """states route"""
    states = [state for state in storage.all(State).values()]
    return render_template("7-states_list.html", states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
