# Web Flask

Date: 2025-06-06 11:13:06 +0300

## Description
This directory contains Flask web application files for the AirBnB clone project.

## Files
* `__init__.py` - Initializes the Flask application package
* `0-hello_route.py` - Simple Flask app that displays "Hello HBNB!" at route '/'

## Requirements
* Python 3.4.3
* Flask
* All files are PEP8 compliant
* All files are executable
* All modules have documentation
* All functions have documentation

## Testing
Start the Flask application:
```bash
python3 -m web_flask.0-hello_route
```

Test routes:
```bash
curl 0.0.0.0:5000/  # Should display "Hello HBNB!"
curl 0.0.0.0:5000/noroute  # Should return 404 error
``` 