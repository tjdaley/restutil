"""
api.py - Restful API server for my projects.

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import os
import flask
from functools import wraps
import redis
import time

import util.util as UTIL

from routes.fred_routes import fred_routes
from routes.zillow_routes import zillow_routes
from routes.code_search_routes import code_routes
from services.codesearch import download_index

RATE_LIMIT = 3  # Can make this many calls per second


redis_service = redis.Redis(
    host=UTIL.get_env('REDIS_HOST', 'localhost'),
    port=int(UTIL.get_env('REDIS_PORT', 6379)),
    db=0
)

if UTIL.get_env('DOWNLOAD_INDEX_ON_START') == 'Y':
    UTIL.logmessage('Downloading search index')
    download_index()
    UTIL.logmessage('Search index downloaded')

app = flask.Flask(__name__)
app.register_blueprint(fred_routes)
app.register_blueprint(zillow_routes)
app.register_blueprint(code_routes)


def authentication_failed():
    """
    Constructs a standard failure return.
    """
    return flask.make_response(
        "Could not verify your access key.",
        401,
        {'WWW-Authenticate': 'Basic realm="Access Key Required"'}
    )


def verify_access_token():
    """
    Verify that an access token is valid and enabled.

    Args:
      None.
    Returns:
      None if OK otherwise dict to return as error message
    """
    if not flask.request.authorization:
        return authentication_failed()

    key = f'access_{flask.request.authorization.username}'

    try:
        if int(redis_service.get(key)) == 1:
            result = None
        else:
            result = UTIL.failure_message('Access token not enabled', 'ERR_TOKEN_NOT_ENABLED')
    except TypeError:
        result = UTIL.failure_message('Error in access token storage', 'ERR_TOKEN_DATA_TYPE')
    except Exception as e:
        UTIL.logmessage(f"Error retrieving {key}: {str(e)}")
        result = UTIL.failure_message(str(e), 'ERR_GENERAL')
    return result


def verify_rate_limit() -> bool:
    """
    See if a request should be rejected because the account associated
    with *token* has used up all its requests for this timeperiod.

    Args:
      None.
    Returns:
      None if OK otherwise dict to return as error message
    """
    if not flask.request.authorization:
        return authentication_failed()

    token = flask.request.authorization.username
    timestamp = int(time.time())
    key = f'rate_{token}_{timestamp}'
    pipe = redis_service.pipeline()
    pipe.incr(key)
    pipe.expire(key, 1)
    result = pipe.execute()
    if result[0] >= RATE_LIMIT:
        return UTIL.failure_message("Rate Limited", "ERR_RATE_LIMIT")
    return None


# List of functions that will be called before every request.
app.before_request_funcs = {
    None: [verify_access_token, verify_rate_limit]
}


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
    message = UTIL.success_message()
    message['message'] = "Hello, World!!"
    return message


@app.route('/sitemap/<string:service>/<string:query>/', methods=['GET'])
def sitemap_for_service(service, query):
    search = f'/{service}/{query}/'
    results = []
    message = UTIL.success_message()
    for rule in app.url_map.iter_rules():
        rule_str = str(rule)
        if rule_str.startswith(search):
            results.append(rule_str)
    message['data'] = results
    return flask.jsonify(message)


@app.route('/sitemap', methods=['GET'])
def sitemap():
    return flask.jsonify(list_routes())


PORT = UTIL.get_env('LISTEN_PORT', 8005)
DEBUG = UTIL.get_env_bool('FLASK_DEBUG', False)
UTIL.logmessage(f"Listening on {PORT}.")
app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
