"""
api.py - Restful API server for my projects.

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import os
import flask

import util.util as UTIL

VERSION = "0.0.1"

app = flask.Flask(__name__)
app.config['DEBUG'] = UTIL.get_env_bool('FLASK_DEBUG', False)


@app.route('/', methods=['GET'])
def home():
    return {'success': True, 'message': "Hello, World.", 'version': VERSION}


port = UTIL.get_env('LISTEN_PORT', 8081)
UTIL.logmessage(f"Listening on {port}.")
app.run(port=port)
