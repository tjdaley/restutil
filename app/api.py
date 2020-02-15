"""
api.py - Restful API server for my projects.

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import os
import flask

import util.util as UTIL

from routes.fred_routes import fred_routes

VERSION = "0.0.1"

app = flask.Flask(__name__)
app.config['DEBUG'] = UTIL.get_env_bool('FLASK_DEBUG', False)
app.register_blueprint(fred_routes)


def list_routes():
    from urllib.parse import unquote
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)

        line = unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)
    return output


@app.route('/', methods=['GET'])
def home():
    return {'success': True, 'message': "Hello, World.", 'version': VERSION}


@app.route('/sitemap', methods=['GET'])
def sitemap():
    return flask.jsonify(list_routes())


port = UTIL.get_env('LISTEN_PORT', 8081)
UTIL.logmessage(f"Listening on {port}.")
app.run(port=port)
