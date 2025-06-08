#!/usr/bin/python3
"""
Flask web application for displaying states.

This module implements a Flask web application that displays a list of all
State objects present in the database. The application uses SQLAlchemy for
database operations and Jinja2 for template rendering.

Routes:
    /states_list: Displays a HTML page with a list of all State objects
                 sorted by name (A->Z)

Configuration:
    - Host: 0.0.0.0
    - Port: 5000
    - Database: Uses storage engine (FileStorage or DBStorage)
    - Session Management: Closes SQLAlchemy Session after each request

Requirements:
    - Flask
    - SQLAlchemy
    - models.storage
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Remove the current SQLAlchemy Session after each request.

    Args:
        exception: Exception object if any occurred during the request
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Display a HTML page with a list of all State objects.

    Returns:
        str: Rendered HTML template with the list of states
    """
    states = storage.all("State")
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
