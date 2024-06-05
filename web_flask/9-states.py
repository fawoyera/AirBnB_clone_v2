#!/usr/bin/python3
"""
    Module script to start a Flask web application
"""
from flask import Flask, render_template
from markupsafe import escape
from models import storage
from models.state import State


app = Flask(__name__)
states = [state for state in storage.all(State).values()]


@app.teardown_appcontext
def tear_down(arg):
    """tear down method"""
    storage.close()


@app.route('/states', strict_slashes=False)
def states_():
    """states route"""
    return render_template("7-states_list.html", states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """states with id route"""
    ids = escape(id) in  [state.id for state in states]
    if ids:
        state = [state for state in states if state.id == escape(id)][0]
    else:
        state = None
    return render_template("9-states.html", state=state, ids=ids)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
