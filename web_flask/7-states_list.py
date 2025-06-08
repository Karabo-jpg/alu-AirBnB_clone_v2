#!/usr/bin/python3
"""
Script that starts a Flask web application for the AirBnB clone v2 project.

This module implements a Flask web application that displays a list of all
State objects present in the database. It uses SQLAlchemy for database
operations and Jinja2 for template rendering.

Requirements:
    - The application must listen on 0.0.0.0, port 5000
    - States must be sorted by name (A->Z)
    - The database connection must be properly closed after each request
    - Templates should be in the web_flask/templates folder

Routes:
    /states_list: Displays a HTML page with a list of all State objects
                 present in the database.

Template Used:
    7-states_list.html: Template file that displays the list of states
                        in an HTML format.
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
    """
    Main Function - Starts the Flask web application.
    
    The application will start listening on 0.0.0.0:5000
    This means it will be accessible from any IP address
    on the machine using port 5000.
    """
    app.run(host='0.0.0.0', port=5000)