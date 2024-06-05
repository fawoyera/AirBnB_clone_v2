#!/usr/bin/python3
"""
    Module script to start a Flask web application
"""
from flask import Flask, render_template
from markupsafe import escape
from models import storage
from models.state import State
from models.amenity import Amenity


app = Flask(__name__)
states = [state for state in storage.all(State).values()]
amenities = [amenity for amenity in storage.all(Amenity).values()]


@app.teardown_appcontext
def tear_down(arg):
    """tear down method"""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """hbnb filters route"""
    return render_template("10-hbnb_filters.html", states=states, amenities=amenities)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
