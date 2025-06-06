#!/usr/bin/python3
"""
Script that starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /states_list: display a HTML page with a list of all State objects.
"""
from flask import Flask, render_template
from models import storage
from models.state import State

# Create Flask application
app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session after each request."""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Display a HTML page with a list of all State objects.

    The states are sorted by name (A->Z).
    Returns:
        HTML page with the list of states.
    """
    states = storage.all(State)
    sorted_states = sorted(states.values(), key=lambda x: x.name)
    return render_template('7-states_list.html', states=sorted_states)


if __name__ == '__main__':
    """Main Function"""
    app.run(host='0.0.0.0', port=5000)