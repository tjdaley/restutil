"""
api.py - Restful API server for my projects.

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import os
import flask

VERSION = "0.0.1"

app = flask.Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET'])
def home():
    return {'success': True, 'message': "Hello, World.", 'version': VERSION}


app.run(port=os.environ.get('LISTEN_PORT'))