#!/usr/bin/python3
"""
Script that starts a Flask web application:
- Your web application must be listening on 0.0.0.0, port 5000
- Routes:
    - /: display "Hello HBNB!"
    - /hbnb: display "HBNB"
    - /c/<text>: display "C " followed by the value of text variable
      (replace underscore _ symbols with a space)
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Display 'Hello HBNB!' when accessing root route."""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Display 'HBNB' when accessing /hbnb route."""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Display 'C' followed by the value of text.
    Replace underscore _ symbols with a space.
    """
    return 'C {}'.format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
